from sqlalchemy import String, Integer, Float, Date, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.models.base import Base
from datetime import date


class Property(Base):

    __tablename__ = "properties"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Basic Info
    property_type: Mapped[str] = mapped_column(String(50))
    built_up_area: Mapped[float] = mapped_column(Float)

    bedrooms: Mapped[int] = mapped_column(Integer)
    bathrooms: Mapped[int] = mapped_column(Integer)

    # Transaction Info
    purchase_date: Mapped[date] = mapped_column(Date)
    purchase_price: Mapped[float]

    sale_listing_date: Mapped[date] = mapped_column(Date,nullable=True)
    sale_asking_price: Mapped[float] = mapped_column(nullable=True)

    # Maintenance
    last_renovation_date: Mapped[date] = mapped_column(Date,nullable=True)
    renovation_description: Mapped[str] = mapped_column(String(255), nullable=True)

    roof_repair_date: Mapped[date] = mapped_column(Date,nullable=True)
    roof_condition: Mapped[str] = mapped_column(String(50))

    # Rental Status
    available_for_rent: Mapped[bool] = mapped_column(Boolean, default=False)
    expected_rent: Mapped[float] = mapped_column(nullable=True)
    rental_available_date: Mapped[date] = mapped_column(Date, nullable=True)

    # -------------------------
    # Foreign Keys
    # -------------------------

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("owners.id", ondelete="CASCADE")
    )

    location_id: Mapped[int] = mapped_column(
        ForeignKey("locations.id", ondelete="CASCADE"),
        unique=True   # ONE property = ONE location
    )

    # -------------------------
    # Relationships
    # -------------------------

    owner = relationship(
        "Owner",
        back_populates="properties"
    )

    location = relationship (
        "Location",
        back_populates="property",
        uselist=False,
    )

    insurance_records = relationship(
        "InsuranceDetails",
        back_populates="property",
        cascade="all, delete-orphan"
    )