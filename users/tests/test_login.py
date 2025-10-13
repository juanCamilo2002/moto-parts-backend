import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import User

@pytest.mark.django_db
def test_login_returns_access_and_refresh_tokens():
    user = User.objects.create_user(email="juan@example.com", password="test1234")
    client = APIClient()

    url = reverse('users:token_obtain_pair')
    response = client.post(url, {"email": "juan@example.com", "password": "test1234"})

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data