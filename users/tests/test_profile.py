import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken

@pytest.mark.django_db
def test_profile_requires_authentication():
    client = APIClient()
    response = client.get(reverse('users:profile'))
    assert response.status_code == 401

@pytest.mark.django_db
def test_profile_returns_user_data():
    user = User.objects.create_user(email="user@test.com", password="12345", first_name="Juan")
    refresh = RefreshToken.for_user(user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    response = client.get(reverse('users:profile'))
    assert response.status_code == 200
    assert response.data['email'] == 'user@test.com'