from django.core.management.base import BaseCommand
from users.models import User

class Command(BaseCommand):
    help = 'Create users demo for tests'

    def handle(self, *args, **kwargs):
        admin, _ = User.objects.get_or_create(
            email="admin@moto.com",
            defaults={"password": "admin123", "is_staff": True, "is_superuser": True, "role": "admin"},
        )

        admin.set_password(admin.password)
        admin.save()
        seller, _ = User.objects.get_or_create(
            email="vendedor@moto.com",
            defaults={"password": "seller123", "role": "seller"},
        )
        seller.set_password(seller.password)
        seller.save()
        self.stdout.write(self.style.SUCCESS("✅ Usuarios demo creados correctamente"))