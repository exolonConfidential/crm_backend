from pydantic import BaseModel
from app.schemas.location_schema import LocationResponse
from app.schemas.owner_schema import OwnerResponse
from app.schemas.property_schema import PropertyResponse


class FullEntryCreateResponse(BaseModel):
    location: LocationResponse
    owner: OwnerResponse
    property: PropertyResponse

    class Config:
        from_attributes = True