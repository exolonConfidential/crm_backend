from pydantic import BaseModel
from datetime import date


class PropertyUpdate(BaseModel):
    property_type: str | None = None
    built_up_area: float | None = None

    bedrooms: int | None = None
    bathrooms: int | None = None

    purchase_date: date | None = None
    purchase_price: float | None = None

    sale_listing_date: date | None = None
    sale_asking_price: float | None = None

    last_renovation_date: date | None = None
    renovation_description: str | None = None

    roof_repair_date: date | None = None
    roof_condition: str | None = None

    available_for_rent: bool | None = None
    expected_rent: float | None = None
    rental_available_date: date | None = None