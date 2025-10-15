import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from users.models import User
from orders.models import Order
from customers.models import Customer

@pytest.mark.django_db
def test_seller_can_list_and_update_orders():
    seller = User.objects.create_user(email="seller@test.com", password="12345")
    refresh = RefreshToken.for_user(seller)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    customer = Customer.objects.create(
        customer_type='individual',
        first_name='Carlos',
        last_name='Martínez',
        identification_type='CC',
        identification_number='1111111111',
        seller=seller
    )

    order = Order.objects.create(customer=customer, seller=seller, total=100000)

    # read
    list_url = reverse('orders:order-list')
    response = client.get(list_url)
    assert response.status_code == 200
    assert len(response.data) > 0

    # update status
    detail_url = reverse('orders:order-detail', args=[order.id])
    response = client.patch(detail_url, {'status': 'COMPLETED'}, format='json')
    assert response.status_code == 200
    order.refresh_from_db()
    assert order.status == 'COMPLETED'