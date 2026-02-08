from pydantic import BaseModel


class LocationCreate(BaseModel):
    place_id: int
    osm_id: int
    osm_type: str

    latitude: float
    longitude: float

    house_number: str | None = None
    road: str
    city: str
    county: str
    state: str
    postcode: str
    country: str
    country_code: str

    display_name: str

    bbox_lat_min: float
    bbox_lat_max: float
    bbox_lon_min: float
    bbox_lon_max: float