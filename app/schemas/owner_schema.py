from pydantic import BaseModel


class OwnerResponse(BaseModel):
    id: int
    full_name: str
    phone_number: str
    email: str
    occupation: str
    annual_income_range: str
    willing_to_rent: bool
    desired_rent_price: int | None
    willing_to_sell: bool
    desired_sell_price: int | None

    class Config:
        from_attributes = True