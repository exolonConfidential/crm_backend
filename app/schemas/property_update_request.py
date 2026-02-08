from pydantic import BaseModel
from app.schemas.owner_update_schema import OwnerUpdate
from app.schemas.property_update_schema import PropertyUpdate


class PropertyOwnerUpdateRequest(BaseModel):
    owner: OwnerUpdate | None = None
    property: PropertyUpdate | None = None