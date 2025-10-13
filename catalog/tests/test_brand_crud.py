import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from catalog.models import Brand
from django.urls import reverse

@pytest.mark.django_db
def test_admin_can_crud_brands():
    admin = User.objects.create_user(email="admin@test.com", password="12345", role="admin")
    refresh = RefreshToken.for_user(admin)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    # CREATE
    list_url = reverse("catalog:brand-list")
    create_response = client.post(list_url, {"name": "Michelin", "country": "Francia"}, format="json")
    assert create_response.status_code == 201
    brand_id = create_response.data["id"]

    # READ
    detail_url = reverse("catalog:brand-detail", args=[brand_id])
    get_response = client.get(detail_url)
    assert get_response.status_code == 200
    assert get_response.data["name"] == "Michelin"

    # UPDATE
    update_response = client.put(detail_url, {"name": "Michelin Tires", "country": "France"}, format="json")
    assert update_response.status_code == 200
    assert update_response.data["name"] == "Michelin Tires"

    # DELETE
    delete_response = client.delete(detail_url)
    assert delete_response.status_code == 204


@pytest.mark.django_db
def test_seller_cannot_modify_brands():
    seller = User.objects.create_user(email="seller@test.com", password="12345", role="seller")
    brand = Brand.objects.create(name="Yamaha", country="Japón")
    refresh = RefreshToken.for_user(seller)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    list_url = reverse("catalog:brand-list")
    detail_url = reverse("catalog:brand-detail", args=[brand.id])

    # Puede listar
    list_response = client.get(list_url)
    assert list_response.status_code == 200

    # No puede crear
    create_response = client.post(list_url, {"name": "Honda"}, format="json")
    assert create_response.status_code == 403

    # No puede eliminar
    delete_response = client.delete(detail_url)
    assert delete_response.status_code == 403