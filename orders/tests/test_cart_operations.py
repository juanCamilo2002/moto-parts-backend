import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from users.models import User
from catalog.models import Brand, Category, Product
from orders.models import Cart, CartItem
from customers.models import Customer

@pytest.mark.django_db
def test_add_and_remove_cart_items():
    seller = User.objects.create_user(email="seller@test.com", password="12345")
    customer = Customer.objects.create(
        customer_type="individual",
        first_name="Juan",
        last_name="Pérez",
        identification_type="CC",
        identification_number="1234567890",
        seller=seller
    )


    brand = Brand.objects.create(name="Yamalube")
    category = Category.objects.create(name="Aceites")
    product = Product.objects.create(
        name="Aceite Yamalube",
        price=60000,
        stock=5,
        brand=brand,
        category=category,
        created_by=seller
    )

    refresh = RefreshToken.for_user(seller)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    cart_url = reverse('orders:cart-list')

    # crear carrito
    data = {
        'customer_id': customer.id,
        'items': [
            {'product_id': product.id, 'quantity': 2, 'price': 50000}
        ]
    }

    response = client.post(cart_url, data, format="json")
    assert response.status_code == 201
    assert Cart.objects.count() == 1
    assert CartItem.objects.count() == 1
    # cart_id = response.data["id"]

    # # agregar producto
    # add_url = reverse('orders:cartitem-list', args=[cart_id])
    # response = client.post(add_url, {"product": product.id, "quantity": 2}, format="json")
    # assert response.status_code == 201
    # assert CartItem.objects.count() == 1

    # # eliminar producto
    # cart_item = CartItem.objects.first()
    # delete_url = reverse('orders:cartitem-detail', args=[cart_id, cart_item.id])
    # response = client.delete(delete_url)
    # assert response.status_code in [204, 200]