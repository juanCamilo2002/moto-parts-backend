from django.core.management.base import BaseCommand
from catalog.models import Brand, Category, Product
from users.models import User

class Command(BaseCommand):
    help = 'Create brands, categories and products demo'

    def handle(self, *args, **kwargs):
        seller = User.objects.filter(role='seller').first()
        if not seller:
            self.stdout.write(self.style.WARNING("⚠️ No existe un usuario vendedor. Ejecuta primero seed_users"))
            return

        brands = [
            ("Honda", "Japón"),
            ("Yamaha", "Japón"),
            ("Suzuki", "Japón"),
            ("Kawasaki", "Japón"),
        ]
        for name, country in brands:
            Brand.objects.get_or_create(name=name, defaults={"country": country})

        categories = [
            ("Motor", "Piezas del motor"),
            ("Frenos", "Sistema de frenos"),
            ("Eléctrico", "Sistema eléctrico"),
            ("Suspensión", "Suspensión y amortiguadores"),
            ("Transmisión", "Transmisión y embrague")
        ]
        for name, description in categories:
            Category.objects.get_or_create(name=name, defaults={"description": description})

        products = [
            ("Filtro Aceite Honda ", 15.99, "Motor", "Honda"),
            ("Pastillas de Freno Delantero Yamaha", 45.99, "Frenos", "Yamaha"),
            ("Batería 12V Kawasaki", 89.99, "Eléctrico", "Kawasaki"),
            ("Amortiguador Trasero Suzuki", 299.99, 'Suspensión', 'Suzuki')
        ]
        for name, price, category_name, brand_name in products:
            category = Category.objects.get(name=category_name)
            brand = Brand.objects.get(name=brand_name)
            Product.objects.get_or_create(
                name=name,
                defaults={"price": price, "stock": 15, "brand": brand, "category": category, "created_by": seller},
            )

        self.stdout.write(self.style.SUCCESS("✅ Catálogo cargado correctamente"))