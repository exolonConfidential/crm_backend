from pydantic import BaseModel, Field

class NearestAssetRequest(BaseModel):

    lat: float = Field(..., ge=-90, le=90, example=34.01544)
    lng: float = Field(..., ge=-180, le=180, example=-118.2201)
