import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from customers.models import Customer
from django.urls import reverse


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(email="admin@test.com", password="12345")


@pytest.fixture
def seller_user(db):
    return User.objects.create_user(email="seller@test.com", password="12345")


@pytest.fixture
def auth_client(api_client):
    """Returns an authenticated client with a given user."""
    def _auth_client(user):
        refresh = RefreshToken.for_user(user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        return api_client
    return _auth_client


# any user auth can can create customers
@pytest.mark.django_db
@pytest.mark.parametrize("user_role", ["admin", "seller"])
def test_authenticated_user_can_create_customer(auth_client, user_role):
    user = (
        User.objects.create_superuser(email="admin@test.com", password="12345")
        if user_role == "admin"
        else User.objects.create_user(email="seller@test.com", password="12345")
    )

    client = auth_client(user)
    url = reverse("customers:customer-list")

    data = {
        "customer_type": "individual",
        "first_name": "Juan",
        "last_name": "Pérez",
        "identification_type": "CC",
        "identification_number": "1234567890",
        "phone": "3001234567",
        "email": "juanperez@example.com",
    }

    response = client.post(url, data, format="json")
    assert response.status_code == 201, f"Error con usuario {user_role}"
    assert Customer.objects.count() == 1

# any user auth can can list customers
@pytest.mark.django_db
@pytest.mark.parametrize("user_role", ["admin", "seller"])
def test_authenticated_user_can_list_customers(auth_client, user_role):
    user = (
        User.objects.create_superuser(email="admin@test.com", password="12345")
        if user_role == "admin"
        else User.objects.create_user(email="seller@test.com", password="12345")
    )

    Customer.objects.create(
        customer_type="individual",
        first_name="Laura",
        last_name="Mora",
        identification_type="CC",
        identification_number="12345",
        seller=user
    )

    client = auth_client(user)
    url = reverse("customers:customer-list")
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data) >= 1


# any user auth can can update a customer
@pytest.mark.django_db
@pytest.mark.parametrize("user_role", ["admin", "seller"])
def test_authenticated_user_can_update_customer(auth_client, user_role):
    seller = User.objects.create_user(email="seller@test.com", password="12345")
    customer = Customer.objects.create(
        customer_type="individual",
        first_name="Santiago",
        last_name="Ruiz",
        identification_type="CC",
        identification_number="1111111111",
        seller=seller,
    )

    user = (
        User.objects.create_superuser(email="admin@test.com", password="12345")
        if user_role == "admin"
        else seller
    )

    client = auth_client(user)
    url = reverse("customers:customer-detail", args=[customer.id])
    response = client.patch(url, {"phone": "3020000000"}, format="json")

    assert response.status_code in [200, 204]
    updated_customer = Customer.objects.get(id=customer.id)
    assert updated_customer.phone == "3020000000"


# any user auth can can delete a customer
@pytest.mark.django_db
@pytest.mark.parametrize("user_role", ["admin", "seller"])
def test_authenticated_user_can_delete_customer(auth_client, user_role):
    seller = User.objects.create_user(email="seller@test.com", password="12345")
    customer = Customer.objects.create(
        customer_type="individual",
        first_name="María",
        last_name="López",
        identification_type="CC",
        identification_number="5555555555",
        seller=seller,
    )

    user = (
        User.objects.create_superuser(email="admin@test.com", password="12345")
        if user_role == "admin"
        else seller
    )

    client = auth_client(user)
    url = reverse("customers:customer-detail", args=[customer.id])
    response = client.delete(url)

    assert response.status_code == 204
    assert not Customer.objects.filter(id=customer.id).exists()
