from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from .models import Cart,  Order
from .serializers import CartSerializer, OrderSerializer

@extend_schema(tags=['Pedidos'], summary="Gestión del carrito de compras")
class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return Cart.objects.filter(customer__seller=self.request.user, is_active=True)
    

@extend_schema(tags=['Pedidos'], summary="Gestión de pedidos")
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Order.objects.all()
        return Order.objects.filter(seller=user)
    
    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)