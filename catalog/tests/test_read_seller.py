import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from catalog.models import Product, Brand, Category
from django.urls import reverse

@pytest.mark.django_db
def test_seller_can_view_but_not_modify_products():
    user = User.objects.create_user(email="seller@test.com", password="12345", role="seller")
    brand = Brand.objects.create(name="Michelin", country="France")
    category = Category.objects.create(name="Llantas", description="Llantas para vehiculos")
    product = Product.objects.create(
        name="Test Product",
        price=45000,
        stock=10,
        created_by=user,
        brand=brand,
        category=category
    )
    
    refresh = RefreshToken.for_user(user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    list_url = reverse('catalog:product-list')
    list_response = client.get(list_url)
    assert list_response.status_code == 200

    detail_url = reverse('catalog:product-detail', args=[product.id])
    detail_response = client.get(detail_url)
    assert detail_response.status_code == 200

    create_response = client.post(list_url, {
        "name": "Filtro de aire",
        "price": 30000,
        "stock": 5,
        "brand_id": brand.id,
        "category_id": category.id
    })

    assert create_response.status_code == 403