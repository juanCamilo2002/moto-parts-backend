import pytest
from users.models import User

@pytest.mark.django_db
def test_user_default_role_is_seller():
    user = User.objects.create_user(email="test@example.com", password="test1234")
    assert user.role == "seller"


@pytest.mark.django_db
def test_superuser_has_admin_role():
    admin = User.objects.create_superuser(email="admin@example.com", password="admin1234")
    assert admin.role == "admin"
    assert admin.is_staff 
    assert admin.is_superuser