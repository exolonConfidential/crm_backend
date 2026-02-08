from pydantic import BaseModel, Field



class MapQueryParams(BaseModel):
    lat: float = Field(..., ge=-90, le=90, description="Latitude")
    lon: float = Field(..., ge=-180, le=180, description="Longitude")
    radius: int = Field(2000, gt=0, le=50000, description="Search radius in meters")



class LocationResponse(BaseModel):
    id: int

    # OSM identifiers
    place_id: int
    osm_id: int
    osm_type: str

    # Coordinates
    latitude: float
    longitude: float

    # Address info
    house_number: str | None = None
    road: str
    city: str
    county: str
    state: str
    postcode: str
    country: str
    country_code: str

    # Display name
    display_name: str

    # Bounding box
    bbox_lat_min: float
    bbox_lat_max: float
    bbox_lon_min: float
    bbox_lon_max: float

    class Config:
        from_attributes = True


class MapQueryResponse(BaseModel):
    total: int
    locations: list[LocationResponse]