from django.core.management.base import BaseCommand
from customers.models import Customer
from users.models import User

class Command(BaseCommand):
    help = "Crea clientes demo"

    def handle(self, *args, **kwargs):
        seller = User.objects.filter(role='seller').first()
        if not seller:
            self.stdout.write(self.style.WARNING("⚠️ No existe un vendedor, ejecuta primero seed_users"))
            return

        Customer.objects.get_or_create(
            customer_type="individual",
            first_name="Juan",
            last_name="Pérez",
            identification_type="CC",
            identification_number="1234567890",
            email='perez@gmail.com',
            seller=seller,
        )

        Customer.objects.get_or_create(
            customer_type="company",
            first_name="Montallantas",
            company_name='Montallantas S.A.S',
            last_name="S.A.S",
            identification_type="NIT",
            identification_number="900123456-7",
            email='montañantas@gmail.com',
            seller=seller,
        )

        self.stdout.write(self.style.SUCCESS("✅ Clientes demo creados correctamente"))
