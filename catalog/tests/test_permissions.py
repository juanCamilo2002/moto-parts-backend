import pytest
from rest_framework.test import APIClient
from django.urls import reverse

@pytest.mark.django_db
def test_unauthenticated_user_cannot_access_product_list():
    client = APIClient()
    url = reverse('catalog:product-list')
    response = client.get(url)
    assert response.status_code == 401