from app.repositories.property_repo import find_nearest_property_and_owner

def get_nearest_asset(driver, lat: float, lng: float):

    data = find_nearest_property_and_owner(driver, lat, lng)

    if not data:
        raise ValueError("No nearby property found")

    return data
