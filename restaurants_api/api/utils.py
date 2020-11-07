"""Some utils functions module."""
from math import sin, cos, sqrt, atan2, radians

from django.conf import settings

from api.models import Restaurant


def compute_geo_coordinates_distance(lng_1, lat_1, lng_2, lat_2) -> float:
    """Compute in kilometer the distance between two geo coordinates.
    
    Arguments:
        - lng_1: the longitude of the first coordinate
        - lat_1: the latitude of the first coordinate
        - lng_2: the longitude of the second coordinate
        - lat_2: the latitude of the second coordinate
    """
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(lat_1)
    lon1 = radians(lng_1)
    lat2 = radians(lat_2)
    lon2 = radians(lng_2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance


def find_restaurants_neightbords(longitude: float, latitude: float) -> list:
    """get restaurants in 3km around."""
    matched_restaurants: list = []
    restaurants = Restaurant.objects.all()
    for restaurant in restaurants:
        distance: float = compute_geo_coordinates_distance(
            longitude,
            latitude,
            restaurant.longitude,
            restaurant.latitude
        )
        if distance <= settings.RESTAURANT_QUERY_RADIUS_LIMIT:
            matched_restaurants.append({
                'name': restaurant.name,
                'longitude': restaurant.longitude,
                'latitude': restaurant.latitude    
            })
    return matched_restaurants
