from pydantic import BaseModel
from app.schemas.owner_schema import OwnerResponse
from app.schemas.property_schema import PropertyResponse


class PropertyOwnerResponse(BaseModel):
    owner: OwnerResponse
    property: PropertyResponse

    class Config:
        from_attributes = True