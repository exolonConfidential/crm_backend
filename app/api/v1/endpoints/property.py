from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession


from app.db.session import get_async_session
from app.services.property_service import PropertyService
from app.schemas.property_schema import PropertyResponse
from app.schemas.full_entry_schema import FullEntryCreateRequest
from app.schemas.property_update_request import PropertyOwnerUpdateRequest

router = APIRouter(prefix="/property", tags=["Property"])


@router.get("/by-location/{location_id}", response_model=PropertyResponse)
async def get_property_by_location(
    location_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
        Fetch property + owner using location_id.
        Called when agent clicks map box.
    """

    property_obj = await PropertyService.get_property_by_location_id(
        session=session,
        location_id=location_id
    )

    if not property_obj:
        raise HTTPException(
            status_code=404,
            detail="Property not found for given location"
        )

    return property_obj

@router.post("/create-full", response_model=PropertyResponse)
async def create_full_entry(
    payload: FullEntryCreateRequest,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Creates Location + Owner + Property in a single transaction.
    Frontend cannot send IDs.
    """

    try:
        property_obj = await PropertyService.create_full_entry(
            session=session,
            location_data=payload.location,
            owner_data=payload.owner,
            property_data=payload.property,
        )

        return property_obj

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Failed to create property entry"
        )
    
@router.put("/{property_id}", response_model=PropertyResponse)
async def update_property_and_owner(
    property_id: int = Path(..., gt=0),
    payload: PropertyOwnerUpdateRequest = ...,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Update Property + Owner details.
    Partial updates supported.
    """

    if not payload.owner and not payload.property:
        raise HTTPException(
            status_code=400,
            detail="No update data provided"
        )

    property_obj = await PropertyService.update_property_and_owner(
        session=session,
        property_id=property_id,
        owner_data=payload.owner.dict(exclude_unset=True) if payload.owner else None,
        property_data=payload.property.dict(exclude_unset=True) if payload.property else None,
    )

    if not property_obj:
        raise HTTPException(
            status_code=404,
            detail="Property not found"
        )

    return property_obj