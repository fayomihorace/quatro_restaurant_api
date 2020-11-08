"""Api test module."""
from django.urls import reverse, path, include
from django.test.client import encode_multipart, RequestFactory
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.sessions.middleware import SessionMiddleware
from rest_framework.test import force_authenticate
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework.test import force_authenticate
from rest_framework.test import RequestsClient

from api.utils import find_restaurants_neightbords
from api.models import Restaurant
from api import views


factory = RequestFactory()
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

test_coordinates: dict = {
    "lat": 0.0300011,
    "lng": 0.0150021    
}

registration_data: dict = {
	"name": "fayhj",
	"username": "folahan",
	"password": "fayomi"
}

login_data: dict = {
    "username": "folahan",
	"password": "fayomi"
}

SUCCESS_CODE: int = 200

ERROR_CODE: int = 400


class APITestClass(APITestCase):
    """API test class."""

    def _register_user(self, data: dict):
        """registration helper function."""
        request = factory.post('register/', data, format='json')
        response = views.RegisterView.as_view()(request)
        return response

    def _login_user(self, data: dict):
        """login helper function."""
        request = factory.post('login/', data, format='json')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        response = views.LoginView.as_view()(request)
        return response

    def _get_api_keys(self, force_login: bool = False):
        """get api keys function."""
        request = factory.get('api_keys/')
        if force_login:
            force_authenticate(request, user=User.objects.all()[0])
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        response = views.ApiKeysView.as_view()(request)
        return response

    def _create_restaurant_fixtures(self):
        """create reataurants fixtures."""
        for fixture in fixtures:
            Restaurant.objects.create(
                name=fixture['name'],
                longitude=fixture['lng'],
                latitude=fixture['lng'],
            )

    def test_create_account(self):
        """Test registration ."""
        response = self._register_user(registration_data)
        self.assertEqual(response.status_code, SUCCESS_CODE)

    def test_good_login(self):
        """Test login will good credentials."""
        # register user first
        self._register_user(registration_data)
        response = self._login_user(login_data)
        self.assertEqual(response.status_code, SUCCESS_CODE)

    def test_login_login(self):
        """Test login will bad credentials."""
        # register user first
        self._register_user(registration_data)
        login_data['password'] = 'some bad password'
        response = self._login_user(login_data)
        self.assertEqual(response.status_code, ERROR_CODE)

    def test_try_to_fetch_api_keys_without_login(self):
        """Try fetch api without login."""
        # register user first
        self._register_user(registration_data)
        response = self._get_api_keys()
        self.assertNotEqual(response.status_code, SUCCESS_CODE)

    def test_try_to_fetch_api_keys_with_login(self):
        """Try fetch api without login."""
        # register user first
        self._register_user(registration_data)
        response = self._get_api_keys(force_login=True)
        self.assertEqual(response.status_code, SUCCESS_CODE)
        response_data = eval(str(response.content)[2:-1])
        self.assertTrue('public-key' in response_data.keys())
        self.assertTrue('secret-key' in response_data.keys())

    def test_neightbord_restaurant_around_lookup(self):
        """Test fetch restaurants in 3km around."""
        self._create_restaurant_fixtures()
        response: list = [
            {
            "name": "Karim 24",
            "longitude": 0.0250022,
            "latitude": 0.0250022,
            "distance": 1.2435424623272242
            },
            {
            "name": "Zitawi",
            "longitude": 0.0250025,
            "latitude": 0.0250025,
            "distance": 1.2435573902932506
            }
        ]
        self.assertEqual(
            find_restaurants_neightbords(
                test_coordinates['lng'],
                test_coordinates['lat'],    
            ),
            response
        )
