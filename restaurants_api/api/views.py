"""API view."""
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.db.utils import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework_api_key.permissions import BaseHasAPIKey
from rest_framework_api_key.models import APIKey
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.status import HTTP_200_OK

from api.models import UserApiKey
from api.utils import find_restaurants_neightbords


class HasAPIKey(BaseHasAPIKey):
    """Custom API permission checker."""
    model = APIKey

    def get_key(self, request):
        x_public_key: str = request.headers.get('X-Public-Key', '')
        x_xecret_key: str = request.headers.get('X-Secret-Key', '')
        return '{}.{}'.format(x_public_key, x_xecret_key)


class RegisterView(APIView):
    """Registration API class."""
    permission_classes = []
 
    def post(self, request):
        """Register the user."""
        try:
            new_user: User = User(
                first_name=request.data['name'],
                username=request.data['username'],
                password=make_password(request.data['password'])
            )
            new_user.save()
            _, key = APIKey.objects.create_key(
                name="{}-{}".format(new_user.username, new_user.id)
            )
            # As described in djangorestframework-api-key documentation, an API
            # key is composed of two items:
            # A prefix P, which is a generated string of 8 characters.
            # A secret key SK, which is a generated string of 32 characters.
            # The generated key that clients use to make authorized requests is 
            # GK = P.SK. whose value is `key` here
            user_key: UserApiKey = UserApiKey.objects.create(
                user=new_user,
                public_key=key.split('.')[0],
                secret_key=key.split('.')[1]
            )
            return JsonResponse(
                {
                    'success': 'Registration completed',
                    'public-key': user_key.public_key,
                    'secret-key': user_key.secret_key
                },
                status=HTTP_200_OK
            )
        except IntegrityError as e:
            return JsonResponse(
               {'error': 'Invalid Input'},
                status=HTTP_400_BAD_REQUEST
            )


class LoginView(APIView):
    """Login API class."""
    permission_classes = []

    def post(self, request):
        """Login the user."""
        try:
            user: User = User.objects.get(username=request.data['username'])
            if user.check_password(request.data['password']):
                login(request, user)
                return JsonResponse(
                    {'success': 'Login successfully'},
                    status=HTTP_200_OK
                )
        except User.DoesNotExist as e:
            pass

        return JsonResponse(
            {'error': 'Invalid credentials'},
            status=HTTP_400_BAD_REQUEST
        )


class LogoutView(APIView):
    """Logout API class."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Log out the user."""
        logout(request)
        return JsonResponse({'status': 'logout'}, status=HTTP_200_OK)


class ApiKeysView(APIView):
    """api_keys API class."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Retrieve user's api keys."""

        user: User = request.user
        user_key: UserApiKey = UserApiKey.objects.get(user=user,)
        return JsonResponse(
            {
                'public-key': user_key.public_key,
                'secret-key': user_key.secret_key
            },
            status=HTTP_200_OK
        )


@method_decorator(csrf_exempt, name='dispatch')
class RestaurantsView(APIView):
    """Restaurants API class."""
    permission_classes = [HasAPIKey]
    authentication_classes = ()

    def post(self, request):
        """get restaurants around."""
        return JsonResponse(
            {
                'results': find_restaurants_neightbords(
                    request.data['lng'],
                    request.data['lat']
                )
            },
            status=HTTP_200_OK
        )
