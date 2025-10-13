import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from django.urls import reverse

@pytest.mark.django_db
def test_admin_can_crud_products():
    admin = User.objects.create_user(email="admin@test.com", password="12345", role="admin")
    refresh = RefreshToken.for_user(admin)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    list_url = reverse('catalog:product-list')
    create_response = client.post(list_url, {
        "name": "Llanta Michelin",
        "price": 250000,
        "stock": 8
    }, format="json")

    assert create_response.status_code == 201
    product_id = create_response.data['id']

    detail_url = reverse('catalog:product-detail', args=[product_id])
    update_reponse = client.put(detail_url, {"stock": 12}, format="json")
    assert update_reponse.status_code == 200
    assert update_reponse.data['stock'] == 12

    delete_response = client.delete(detail_url)
    assert delete_response.status_code == 204