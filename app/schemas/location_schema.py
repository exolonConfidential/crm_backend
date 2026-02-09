from pydantic import BaseModel
from typing import Optional


class LocationResponse(BaseModel):
    id: int

    # OSM Identifiers
    place_id: int
    osm_id: int
    osm_type: str

    # Coordinates
    latitude: float
    longitude: float

    # Address Info
    house_number: Optional[str]
    road: str
    city: str
    county: str
    state: str
    postcode: str
    country: str
    country_code: str

    # Display name
    display_name: str

    # Bounding Box
    bbox_lat_min: float
    bbox_lat_max: float
    bbox_lon_min: float
    bbox_lon_max: float

    # NOTE:
    # geom intentionally excluded
    # because GeoAlchemy Geography objects don't serialize cleanly in JSON
    # and should be exposed via lat/lng instead

    class Config:
        from_attributes = True