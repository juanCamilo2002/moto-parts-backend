import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from users.models import User
from customers.models import Customer
from catalog.models import Product, Brand, Category
from orders.models import Order, OrderItem


@pytest.mark.django_db
def test_seller_can_create_order_with_items():
    seller = User.objects.create_user(email="seller@test.com", password="12345")

    customer = Customer.objects.create(
        customer_type="individual",
        first_name="Juan",
        last_name="Pérez",
        identification_type="CC",
        identification_number="1234567890",
        seller=seller
    )

    brand = Brand.objects.create(name='Motul', country='Francia')
    category = Category.objects.create(name='Aceites')

    product = Product.objects.create(
        name='Aceite Motul',
        price=50000,
        stock=10,
        brand=brand,
        category=category,
        created_by=seller
    )

    refresh = RefreshToken.for_user(seller)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    url = reverse('orders:order-list')
    data = {
        'customer_id': customer.id,
        'total': 50000,
        'status': 'PENDING',
        'items': [
            {'product_id': product.id, 'quantity': 2, 'price': 50000}
        ]
    }

    response = client.post(url, data, format='json')
    assert response.status_code == 201
    assert Order.objects.count() == 1
    assert OrderItem.objects.count() == 1