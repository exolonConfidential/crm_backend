from app.repositories.location_repo import LocationRepository
from app.repositories.property_repo import PropertyRepository
from app.db.models.owner import Owner
from app.db.models.property import Property
from app.db.models.location import Location

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError


class PropertyService:

    @staticmethod
    async def get_property_by_osm(session, osm_type, osm_id):

        location = await LocationRepository.get_by_osm(
            session, osm_type, osm_id
        )

        if not location:
            return None

        property = await PropertyRepository.get_by_location_id(
            session, location.id
        )

        return property


    @staticmethod
    async def create_full_entry(session, location_data, owner_data, property_data):

        # -------------------------
        # 1. FIND OR VALIDATE OWNER
        # -------------------------

        existing_owner_by_phone = await session.scalar(
            select(Owner).where(Owner.phone_number == owner_data.phone_number)
        )

        existing_owner_by_email = await session.scalar(
            select(Owner).where(Owner.email == owner_data.email)
        )

        if existing_owner_by_phone and existing_owner_by_email:
            # same owner → reuse
            owner = existing_owner_by_phone

        elif existing_owner_by_phone and not existing_owner_by_email:
            raise HTTPException(
                status_code=409,
                detail="Phone number already linked to different email"
            )

        elif existing_owner_by_email and not existing_owner_by_phone:
            raise HTTPException(
                status_code=409,
                detail="Email already linked to different phone number"
            )

        else:
            owner = None

        # -------------------------
        # 2. FIND LOCATION
        # -------------------------

        location = await LocationRepository.get_by_osm(
            session,
            location_data.osm_type,
            location_data.osm_id
        )

        if not location:
            location = await session.scalar(
                select(Location).where(Location.place_id == location_data.place_id)
            )

        # -------------------------
        # 3. CHECK EXISTING PROPERTY
        # -------------------------

        if location:
            existing_property = await PropertyRepository.get_by_location_id(
                session,
                location.id
            )

            if existing_property:
                # idempotent return
                await session.refresh(existing_property, ["owner", "location"])

                return {
                    "location": existing_property.location,
                    "owner": existing_property.owner,
                    "property": existing_property
                }

        # -------------------------
        # 4. CREATE FLOW
        # -------------------------

        try:
            async with session.begin():

                # create owner if not reused
                if not owner:
                    owner = Owner(**owner_data.dict())
                    session.add(owner)
                    await session.flush()

                # create location if not exists
                if not location:
                    location = await LocationRepository.create(
                        session,
                        location_data.dict()
                    )

                # create property
                prop_data = property_data.dict()
                prop_data["owner_id"] = owner.id
                prop_data["location_id"] = location.id

                property_obj = Property(**prop_data)
                session.add(property_obj)

        except IntegrityError:
            # race condition safety
            existing_property = await PropertyRepository.get_by_location_id(
                session,
                location.id
            )

            if existing_property:
                await session.refresh(existing_property, ["owner", "location"])
                return {
                    "location": existing_property.location,
                    "owner": existing_property.owner,
                    "property": existing_property
                }

            raise HTTPException(
                status_code=409,
                detail="Conflict occurred while creating entry"
            )

        # -------------------------
        # 5. RETURN CREATED OBJECT
        # -------------------------

        await session.refresh(property_obj)
        await session.refresh(property_obj, ["owner", "location"])

        return {
            "location": property_obj.location,
            "owner": property_obj.owner,
            "property": property_obj
        }


    @staticmethod
    async def update_property_and_owner(session, property_id, owner_data, property_data):

        # -------------------------
        # 1. LOAD PROPERTY + OWNER
        # -------------------------
        property_obj = await session.get(Property, property_id)

        if not property_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Property with id={property_id} not found"
            )

        # preload owner (avoid lazy async crash)
        await session.refresh(property_obj, attribute_names=["owner"])
        owner = property_obj.owner

        # -------------------------
        # 2. UNIQUENESS CHECKS (OWNER)
        # -------------------------
        if owner_data:

            if "phone_number" in owner_data:
                existing_phone = await session.scalar(
                    select(Owner).where(
                        Owner.phone_number == owner_data["phone_number"],
                        Owner.id != owner.id
                    )
                )
                if existing_phone:
                    raise HTTPException(
                        status_code=409,
                        detail={
                            "error": "UNIQUENESS_CONFLICT",
                            "table": "owners",
                            "field": "phone_number",
                            "value": owner_data["phone_number"]
                        }
                    )

            if "email" in owner_data:
                existing_email = await session.scalar(
                    select(Owner).where(
                        Owner.email == owner_data["email"],
                        Owner.id != owner.id
                    )
                )
                if existing_email:
                    raise HTTPException(
                        status_code=409,
                        detail={
                            "error": "UNIQUENESS_CONFLICT",
                            "table": "owners",
                            "field": "email",
                            "value": owner_data["email"]
                        }
                    )

        # -------------------------
        # 3. APPLY UPDATES
        # -------------------------
        try:
            async with session.begin():

                if owner_data:
                    for k, v in owner_data.items():
                        if k not in {"id"}:
                            setattr(owner, k, v)

                if property_data:
                    for k, v in property_data.items():
                        # block foreign key tampering
                        if k not in {"id", "owner_id", "location_id"}:
                            setattr(property_obj, k, v)

        except IntegrityError:
            raise HTTPException(
                status_code=409,
                detail="Database conflict occurred while updating"
            )

        # -------------------------
        # 4. PRELOAD RELATIONSHIP
        # -------------------------
        await session.refresh(property_obj)
        await session.refresh(property_obj, ["owner"])

        # -------------------------
        # 5. RESPONSE SHAPE
        # -------------------------
        return {
            "owner": property_obj.owner,
            "property": property_obj
        }
        
    
    @staticmethod
    async def get_property_by_location_id(session, location_id: int):

        property_obj = await PropertyRepository.get_by_location_id(
            session, location_id
        )

        if not property_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No property found for location_id={location_id}"
            )

        # preload owner relationship (VERY IMPORTANT)
        await session.refresh(property_obj)
        await session.refresh(property_obj, attribute_names=["owner"])

        return {
            "owner": property_obj.owner,
            "property": property_obj
        }
        


