from django.db import models
from django.conf import settings
from catalog.models import Product
from customers.models import Customer
from decimal import Decimal

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'Cart #{self.id} - {self.customer}'
    
    def get_total(self):
        total = Decimal("0.00")
        for item in self.items.all():
            total += item.product.price * item.quantity
        return total

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'
    

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pendiente'),
        ('PROCESSING', 'En proceso'),
        ('COMPLETED', 'Completado'),
        ('CANCELLED', 'Cancelado')
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Order #{self.id} - {self.status}' 

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'
     