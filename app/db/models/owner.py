from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.models.base import Base


class Owner(Base):

    __tablename__ = "owners"

    id: Mapped[int] = mapped_column(primary_key=True)

    full_name: Mapped[str] = mapped_column(String(150))

    phone_number: Mapped[str] = mapped_column(String(20), unique=True)
    email: Mapped[str] = mapped_column(String(150), unique=True)

    occupation: Mapped[str] = mapped_column(String(100))
    annual_income_range: Mapped[str] = mapped_column(String(50))

    willing_to_rent: Mapped[bool] = mapped_column(default=False)
    desired_rent_price: Mapped[int] = mapped_column(nullable=True)

    willing_to_sell: Mapped[bool] = mapped_column(default=False)
    desired_sell_price: Mapped[int] = mapped_column(nullable=True)

    # Relationship
    properties = relationship(
        "Property",
        back_populates="owner",
        cascade="all, delete"
    )
