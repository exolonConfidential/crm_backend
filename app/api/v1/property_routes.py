import logging
from fastapi import APIRouter, HTTPException
from app.core.neo4j import get_driver
from app.services.property_service import get_nearest_asset
from app.schemas.location_request import NearestAssetRequest
from app.schemas.property_owner_response import NearestAssetResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/properties", tags=["Geo Search"])

@router.post("/nearest", response_model=NearestAssetResponse)
def nearest_property(payload: NearestAssetRequest):

    logger.info(f"Incoming geo request lat={payload.lat}, lng={payload.lng}")

    try:
        driver = get_driver()

        result = get_nearest_asset(driver, payload.lat, payload.lng)

        logger.info("Nearest asset query successful")

        return result

    except ValueError as e:
        logger.warning(f"No asset found: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        logger.exception("Unexpected server error")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )
