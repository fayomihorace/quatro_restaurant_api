"""Resataurant model seed fixtures module."""
from api.models import Restaurant

 
fixtures: dict = [
    {
        'name': 'Karim 24',
        'lng': 0.0250022,
        'lat': 0.0200011
    },
    {
        'name': 'Corneto',
        'lng': 0.250024,
        'lat': 0.200013
    },
    {
        'name': 'Zitawi',
        'lng': 0.0250025,
        'lat': 0.200016
    },
    {
        'name': 'Ci gusta',
        'lng': 0.250052,
        'lat': 0.200051
    }
]
Restaurant.objects.all().delete()
for fixture in fixtures:
    restaurant: Restaurant = Restaurant.objects.create(
        name=fixture['name'],
        longitude=fixture['lng'],
        latitude=fixture['lng'],
    )
print('restaurant fixtures successfully created !!')
