from pydantic import BaseModel
from datetime import date


class PropertyCreate(BaseModel):
    property_type: str
    built_up_area: float

    bedrooms: int
    bathrooms: int

    purchase_date: date
    purchase_price: float

    sale_listing_date: date | None = None
    sale_asking_price: float | None = None

    last_renovation_date: date | None = None
    renovation_description: str | None = None

    roof_repair_date: date | None = None
    roof_condition: str

    available_for_rent: bool = False
    expected_rent: float | None = None
    rental_available_date: date | None = None