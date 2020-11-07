# Sample Restaurant REST API 

Sample Restaurant REST API.

## Installation
Quite straight forward
```
cd restaurants_api
virtualenv env
source env/bin/activate
pip3 install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
```

## Create restaurant fixtures
```
python3 manage.py shell < restaurant_fixtures.py
```

## Run unit tests
```
python3 manage.py test
```

## Manual Test with fixtures data
### start server
```
python3 manage.py runserver
```

### register user
```
Post on http://127.0.0.1:8000/register/
with data
{
	"name": "fayhj",
	"username": "folahan",
	"password": "fayomi"
}


Response exemple:
{
  "success": "Registration completed",
  "public-key": "FZWnA7wu",
  "secret-key": "JyMQ8YgeVjEo6njVkkSeOIXoGTZSGSXs"
}
```

### login user
```
Post on http://127.0.0.1:8000/login/
with data
{
	"username": "folahan",
	"password": "fayomi"
}


Response exemple:
{
  "success": "Login successfully"
}
```

### get api keys
```
Get on http://127.0.0.1:8000/api_keys/

Result exemple:
{
  "public-key": "Pi9N2o5H",
  "secret-key": "59qoXIsGdOFVFQsFy67UGm8g8IILbBLy"
}
```

### returns the list of restaurants in a 3km radius of those coordinates.
```
Post on http://127.0.0.1:8000/restaurants/ 
With
{
	"lat": 0.0300011,
	"lng": 0.0150021
}

headers:
  X-Public-Key: public-key
  X-Secret-Key: secret-key


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
