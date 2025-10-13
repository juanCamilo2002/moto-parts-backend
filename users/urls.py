from django.urls import path
from .views import ResgisterView, ProfileView, LogoutView

app_name = 'users'
urlpatterns = [
    path('register/', ResgisterView.as_view(), name='register'),
    path('me/', ProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
]