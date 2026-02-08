from geoalchemy2 import Geography
from sqlalchemy import String, Integer, Float, BigInteger, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column
from app.db.models.base import Base


class Location(Base):

    __tablename__ = "locations"
    __table_args__ = (
        UniqueConstraint("osm_type", "osm_id", name="uq_osm_location"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # OSM Identifiers
    place_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    osm_id: Mapped[int] = mapped_column(BigInteger)
    osm_type: Mapped[str] = mapped_column(String(20))

    # Coordinates
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)

    # Address Info
    house_number: Mapped[str] = mapped_column(String(20), nullable=True)
    road: Mapped[str] = mapped_column(String(150))
    city: Mapped[str] = mapped_column(String(100))
    county: Mapped[str] = mapped_column(String(100))
    state: Mapped[str] = mapped_column(String(100))
    postcode: Mapped[str] = mapped_column(String(20))
    country: Mapped[str] = mapped_column(String(100))
    country_code: Mapped[str] = mapped_column(String(10))

    # Display name
    display_name: Mapped[str] = mapped_column(String(300))

    # Bounding Box
    bbox_lat_min: Mapped[float] = mapped_column(Float)
    bbox_lat_max: Mapped[float] = mapped_column(Float)
    bbox_lon_min: Mapped[float] = mapped_column(Float)
    bbox_lon_max: Mapped[float] = mapped_column(Float)

    geom: Mapped[str] = mapped_column(
        Geography("POINT", srid=4326)
    )

    property = relationship(
        "Property",
        back_populates="location",
        uselist=False,
        cascade="all, delete-orphan"
    )