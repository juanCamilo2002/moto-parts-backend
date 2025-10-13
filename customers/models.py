from django.db import models
from django.conf import settings

class Customer(models.Model):
    INDIVIDUAL = 'individual'
    COMPANY = 'company'

    CUSTOMER_TYPE_CHOICES = [
        (INDIVIDUAL, 'Individual'),
        (COMPANY, 'Company'),
    ]

    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPE_CHOICES, default=INDIVIDUAL)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    company_name = models.CharField(max_length=255, blank=True)
    identification_type = models.CharField(max_length=50,  choices=[('CC', 'Cédula'), ('NIT', 'NIT')])
    identification_number = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='customers'
    )

    def __str__(self):
        if self.customer_type == self.COMPANY:
            return self.company_name or "Empresa sin nombre"
        return f"{self.first_name} {self.last_name}" or "Cliente sin nombre"