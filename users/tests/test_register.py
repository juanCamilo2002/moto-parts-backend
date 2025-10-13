import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import User

@pytest.mark.django_db
def test_register_user_creates_seller_by_default():
    client = APIClient()
    data = {
        "email": "test@example.com",
        "password": "test1234",
        "first_name": "John",
        "last_name": "Doe"
    }

    url = reverse('users:register')
    response = client.post(url, data)

    assert response.status_code == 201
    user = User.objects.get(email="test@example.com")
    assert user.role == "seller"
    assert user.check_password("test1234")