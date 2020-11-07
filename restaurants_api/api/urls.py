from django.contrib import admin
from django.urls import path
from api import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('api_keys/', views.ApiKeysView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('restaurants/', csrf_exempt(views.RestaurantsView.as_view())),
]
