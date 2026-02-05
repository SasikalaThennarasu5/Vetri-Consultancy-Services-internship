from django.urls import path
from .views import profile_setup
from . import views

app_name = 'profiles'

urlpatterns = [
    path("me/", views.profile_view, name="view"),
    path('profile/setup/', profile_setup, name='setup'),
]
