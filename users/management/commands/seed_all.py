from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command

class Command(BaseCommand):
    help = "Ejecuta todos los seeders del proyecto en orden (users → catalog → customers → orders)"

    def handle(self, *args, **options):
        try:
            self.stdout.write(self.style.NOTICE("🚀 Iniciando seeders de MotoParts..."))

            # 1️⃣ Usuarios (primero, porque los demás dependen de esto)
            self.stdout.write(self.style.NOTICE("\n➡️ Cargando usuarios..."))
            call_command("seed_users")

              # 3️⃣ Clientes
            self.stdout.write(self.style.NOTICE("\n➡️ Cargando clientes..."))
            call_command("seed_customers")

            # 2️⃣ Catálogo (productos, marcas, categorías)
            self.stdout.write(self.style.NOTICE("\n➡️ Cargando catálogo..."))
            call_command("seed_catalog")

          

            # 4️⃣ Pedidos
            # self.stdout.write(self.style.NOTICE("\n➡️ Cargando pedidos..."))
            # call_command("seed_orders")

            self.stdout.write(self.style.SUCCESS("\n✅ Seeders ejecutados correctamente en orden."))

        except CommandError as e:
            self.stdout.write(self.style.ERROR(f"❌ Error al ejecutar seeders: {e}"))
