import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken

@pytest.mark.django_db
def test_logout_requires_refresh_token():
    user = User.objects.create_user(email="juan@example.com", password="12345")
    refresh = RefreshToken.for_user(user)

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    url = reverse('users:logout')
    response = client.post(url, {})

    assert response.status_code == 400
    assert "obligatorio" in response.data["detail"]


@pytest.mark.django_db
def test_logout_blacklists_token_successfully():
    user = User.objects.create_user(email="juan@example.com", password="12345")
    refresh = RefreshToken.for_user(user)

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    url = reverse('users:logout')
    response = client.post(url, {"refresh": str(refresh)})

    assert response.status_code == 205