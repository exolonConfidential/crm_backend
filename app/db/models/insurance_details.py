from datetime import date
from sqlalchemy import (
    String,
    Integer,
    Boolean,
    Date,
    ForeignKey,
    Text
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.models.base import Base


class InsuranceDetails(Base):

    __tablename__ = "insurance_details"

    id: Mapped[int] = mapped_column(primary_key=True)

    # 🔗 Relation with Property
    property_id: Mapped[int] = mapped_column(
        ForeignKey("properties.id", ondelete="CASCADE"),
        index=True
    )

    # -----------------------------
    # REQUIRED FIELDS (Your spec)
    # -----------------------------

    insurance_company: Mapped[str] = mapped_column(String(150))

    claim_number: Mapped[str] = mapped_column(String(100), unique=True)

    date_of_loss: Mapped[date] = mapped_column(Date)

    adjuster_name: Mapped[str] = mapped_column(String(150), nullable=True)
    adjuster_phone: Mapped[str] = mapped_column(String(30), nullable=True)
    adjuster_email: Mapped[str] = mapped_column(String(150), nullable=True)

    claim_filed: Mapped[bool] = mapped_column(Boolean, default=False)
    claim_approved: Mapped[bool] = mapped_column(Boolean, default=False)

    # -----------------------------
    # 🇺🇸 US Insurance Standard Fields
    # -----------------------------

    policy_number: Mapped[str] = mapped_column(String(100), nullable=True)

    coverage_type: Mapped[str] = mapped_column(
        String(50), nullable=True
    )
    # e.g. Homeowners, Flood, Fire, Liability, Windstorm

    claim_type: Mapped[str] = mapped_column(
        String(50), nullable=True
    )
    # e.g. Roof Damage, Water Damage, Fire, Storm, Theft

    deductible_amount: Mapped[int] = mapped_column(nullable=True)

    claim_amount: Mapped[int] = mapped_column(nullable=True)

    approved_amount: Mapped[int] = mapped_column(nullable=True)

    payment_status: Mapped[str] = mapped_column(
        String(50), nullable=True
    )
    # Pending / Paid / Denied / Under Review

    date_claim_filed: Mapped[date] = mapped_column(Date, nullable=True)

    date_claim_closed: Mapped[date] = mapped_column(Date, nullable=True)

    insurance_agent_name: Mapped[str] = mapped_column(String(150), nullable=True)
    insurance_agent_phone: Mapped[str] = mapped_column(String(30), nullable=True)

    notes: Mapped[str] = mapped_column(Text, nullable=True)

    # -----------------------------
    # Relationship
    # -----------------------------

    property = relationship("Property", back_populates="insurance_records")