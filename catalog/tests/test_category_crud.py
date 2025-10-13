import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User 
from catalog.models import Category
from django.urls import reverse

@pytest.mark.django_db
def test_admin_can_crud_categories():
    admin = User.objects.create_superuser(email="admin@test.com", password="12345")
    refresh = RefreshToken.for_user(admin)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    list_url = reverse('catalog:category-list')
    
    # Create Category
    create_response = client.post(list_url, {"name": "Llantas", "description": "Todo tipo de llantas"}, format="json")
    assert create_response.status_code == 201
    category_id = create_response.data['id']

    # Read Category
    detail_url = reverse('catalog:category-detail', args=[category_id])
    get_response = client.get(detail_url)
    assert get_response.status_code == 200
    assert get_response.data['name'] == "Llantas"

    # Update Category
    update_response = client.put(detail_url,  {"name": "Llantas Premium", "description": "Alta calidad"}, format="json")
    assert update_response.status_code == 200
    assert update_response.data["name"] == "Llantas Premium"

    # Delete Category
    delete_response = client.delete(detail_url)
    assert delete_response.status_code == 204

@pytest.mark.django_db
def test_seller_cannot_crud_categories():
    seller = User.objects.create_user(email="seller@test.com", password="12345")
    category = Category.objects.create(name="Aceites", description="Aceites sintéticos")
    refresh = RefreshToken.for_user(seller)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    list_url = reverse('catalog:category-list')
    detail_url = reverse('catalog:category-detail', args=[category.id])

    # can list categories
    list_response = client.get(list_url)
    assert list_response.status_code == 200

    # can retrieve category
    get_response = client.get(detail_url)
    assert get_response.status_code == 200

    # cannot create category
    create_response = client.post(list_url, {"name": "Frenos", "description": "Pastillas de freno"}, format="json")
    assert create_response.status_code == 403

    # cannot update category
    update_response = client.put(detail_url,  {"name": "Frenos Premium", "description": "Alta calidad"}, format="json")
    assert update_response.status_code == 403

    # cannot delete category
    delete_response = client.delete(detail_url)
    assert delete_response.status_code == 403
    