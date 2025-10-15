import pytest
from rest_framework.test import APIClient
from django.urls import reverse

@pytest.mark.django_db
def test_unauthenticated_user_cannot_create_order():
    client = APIClient()
    url = reverse('orders:order-list')
    response = client.post(url, {
        "customer": 1,
        "seller": 1,
        "total": 100000,
        "status": "PENDING"
    }, format='json')

    assert response.status_code == 401