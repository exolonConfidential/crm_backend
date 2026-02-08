from pydantic import BaseModel


class OwnerUpdate(BaseModel):
    full_name: str | None = None
    phone_number: str | None = None
    email: str | None = None
    occupation: str | None = None
    annual_income_range: str | None = None

    willing_to_rent: bool | None = None
    desired_rent_price: int | None = None

    willing_to_sell: bool | None = None
    desired_sell_price: int | None = None