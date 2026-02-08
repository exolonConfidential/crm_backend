from pydantic import BaseModel


class OwnerCreate(BaseModel):
    full_name: str
    phone_number: str
    email: str
    occupation: str
    annual_income_range: str

    willing_to_rent: bool = False
    desired_rent_price: int | None = None

    willing_to_sell: bool = False
    desired_sell_price: int | None = None