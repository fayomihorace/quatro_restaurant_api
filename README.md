# Sample Restaurant REST API 

Sample Restaurant REST API.

## Installation
Quite straight forward
```
virtualenv env
source env/bin/activate
pip3 install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py shell < restaurant_fixtures.py
```

## Create restaurant fixtures
```
python3 manage.py shell < restaurant_fixtures.py
```

## Create a user using a client (insomnia, postman ...)
```
python3 manage.py shell < restaurant_fixtures.py
```

## Run unit tests
```
python3 manage.py test
```

## Manual Test with fixtures data
```
input to http://127.0.0.1:8000/restaurants/
{
	"lat": 0.0300011,
	"lng": 0.0150021
}

Results
{
  "results": [
    {
      "name": "Karim 24",
      "longitude": 0.0250022,
      "latitude": 0.0250022
    },
    {
      "name": "Zitawi",
      "longitude": 0.0250025,
      "latitude": 0.0250025
    }
  ]
}
```