from app.repositories.location_repo import LocationRepository
from app.repositories.property_repo import PropertyRepository
from app.db.models.owner import Owner
from app.db.models.property import Property


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

        async with session.begin():

            #  Check existing location
            location = await LocationRepository.get_by_osm(
                session,
                location_data.osm_type,
                location_data.osm_id
            )

            if not location:
                location = await LocationRepository.create(
                    session,
                    location_data.dict()
                )

            # Check if property already exists for this location
            existing_property = await PropertyRepository.get_by_location_id(
                session,
                location.id
            )

            if existing_property:
                # return existing instead of crashing
                return existing_property

            # Create owner
            owner = Owner(**owner_data.dict())
            session.add(owner)
            await session.flush()

            # Create property
            prop_data = property_data.dict()
            prop_data["owner_id"] = owner.id
            prop_data["location_id"] = location.id

            property_obj = Property(**prop_data)
            session.add(property_obj)

        return property_obj
    
    @staticmethod
    async def update_property_and_owner(session, property_id, owner_data, property_data):

        async with session.begin():

            property_obj = await session.get(Property, property_id)

            if not property_obj:
                return None

            owner = property_obj.owner

            # Update owner
            if owner_data:
                for k, v in owner_data.items():
                    setattr(owner, k, v)

            # Update property
            if property_data:
                for k, v in property_data.items():
                    setattr(property_obj, k, v)

        return property_obj
    
    @staticmethod
    async def get_property_by_location_id(session, location_id: int):

        property_obj = await PropertyRepository.get_by_location_id(
            session, location_id
        )

        return property_obj
    


