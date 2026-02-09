from pydantic import BaseModel
from datetime import date
from app.schemas.owner_schema import OwnerResponse


class PropertyResponse(BaseModel):
    id: int

    property_type: str
    built_up_area: float
    bedrooms: int
    bathrooms: int

    purchase_date: date
    purchase_price: float

    sale_listing_date: date | None
    sale_asking_price: float | None

    last_renovation_date: date | None
    renovation_description: str | None

    roof_repair_date: date | None
    roof_condition: str

    available_for_rent: bool
    expected_rent: float | None
    rental_available_date: date | None


    class Config:
        from_attributes = True