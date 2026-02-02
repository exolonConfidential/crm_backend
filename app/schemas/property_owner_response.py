from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# -----------------------------
# Owner Response Schema
# -----------------------------

class OwnerResponse(BaseModel):

    owner_id: str = Field(..., example="OWN_9001")

    full_name: str = Field(..., example="Michael Anderson")

    email: Optional[str] = Field(None, example="michael.anderson@email.com")

    phone: Optional[str] = Field(None, example="+14155552671")

    entity_type: str = Field(..., example="Individual")

    mailing_address: Optional[str] = Field(
        None,
        example="742 Evergreen Terrace, San Diego, CA 92101"
    )

    credit_score_est: Optional[int] = Field(None, ge=300, le=850, example=780)

    income_bracket: Optional[str] = Field(None, example="$100k+")

    net_worth_est: Optional[int] = Field(None, example=1250000)

    portfolio_size: Optional[int] = Field(None, example=3)

    min_price_expectation: Optional[int] = Field(None, example=650000)

    preferred_close_days: Optional[int] = Field(None, example=30)

    urgency_score: Optional[int] = Field(None, ge=0, le=100, example=72)

    is_absentee: Optional[bool] = Field(None, example=True)

    willing_to_sell: Optional[bool] = Field(None, example=True)

    willing_to_partner: Optional[bool] = Field(None, example=False)

    # ⚠ Recommended: Do not expose in public APIs
    tax_id_hash: Optional[str] = Field(
        None,
        example="HASHX9921",
        description="Hashed tax identifier (masked)"
    )

    class Config:
        from_attributes = True


# -----------------------------
# Property Response Schema
# -----------------------------

class PropertyResponse(BaseModel):

    property_id: str = Field(..., example="PROP_1001")

    internal_asset_code: str = Field(..., example="ASSET-LA-7782")

    structure_type: str = Field(..., example="SingleFamily")

    listing_status: str = Field(..., example="ForSale")

    occupancy_status: str = Field(..., example="OwnerOccupied")

    property_grade: str = Field(..., example="A")

    energy_rating: Optional[str] = Field(None, example="B+")

    year_built: int = Field(..., example=2006)

    floors_count: int = Field(..., example=2)

    bedrooms: int = Field(..., example=4)

    bathrooms: int = Field(..., example=3)

    total_built_sqft: int = Field(..., example=2480)

    lot_size_sqft: Optional[int] = Field(None, example=6200)

    garage_spaces: Optional[int] = Field(None, example=2)

    purchase_price: Optional[int] = Field(None, example=590000)

    expected_sale_price: Optional[int] = Field(None, example=740000)

    market_value_est: Optional[int] = Field(None, example=685000)

    current_rent: Optional[int] = Field(None, example=0)

    rental_yield_percent: Optional[float] = Field(None, example=6.2)

    vacancy_days: Optional[int] = Field(None, example=0)

    tenant_present: Optional[bool] = Field(None, example=False)

    # Structural / Condition

    exterior_condition: Optional[str] = Field(None, example="Good")

    foundation_type: Optional[str] = Field(None, example="Slab")

    roof_type: Optional[str] = Field(None, example="Gable")

    roof_material: Optional[str] = Field(None, example="Asphalt Shingle")

    roof_condition: Optional[str] = Field(None, example="Good")

    roof_pitch: Optional[str] = Field(None, example="Medium")

    roof_age_years: Optional[int] = Field(None, example=7)

    siding_material: Optional[str] = Field(None, example="Hardie Board")

    gutter_status: Optional[str] = Field(None, example="Functional")

    hvac_type: Optional[str] = Field(None, example="Central")

    electric_type: Optional[str] = Field(None, example="Copper")

    plumbing_type: Optional[str] = Field(None, example="PEX")

    solar_installed: Optional[bool] = Field(None, example=False)

    # Risk Indicators

    mold_risk_level: Optional[str] = Field(None, example="Low")

    termite_risk_level: Optional[str] = Field(None, example="Low")

    structural_risk_level: Optional[str] = Field(None, example="Low")

    fire_damage_flag: Optional[bool] = Field(None, example=False)

    water_damage_flag: Optional[bool] = Field(None, example=False)

    # Timestamps

    created_at: Optional[datetime] = Field(
        None,
        example="2026-01-29T16:43:44.285Z"
    )

    updated_at: Optional[datetime] = Field(
        None,
        example="2026-01-29T16:43:44.285Z"
    )

    class Config:
        from_attributes = True


# -----------------------------
# Final Nearest Asset Response
# -----------------------------

class NearestAssetResponse(BaseModel):

    owner: OwnerResponse

    property: PropertyResponse

    distanceMeters: float = Field(..., example=342.55)
