from pydantic import BaseModel
from app.schemas.location_create_schema import LocationCreate
from app.schemas.owner_create_schema import OwnerCreate
from app.schemas.property_create_schema import PropertyCreate


class FullEntryCreateRequest(BaseModel):
    location: LocationCreate
    owner: OwnerCreate
    property: PropertyCreate