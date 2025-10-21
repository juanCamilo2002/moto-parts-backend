from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from .models import Cart,  Order
from .serializers import CartSerializer, OrderSerializer
from catalog.models import Product
from customers.models import Customer

@extend_schema(tags=['Pedidos'], summary="Gestión del carrito de compras")
class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return Cart.objects.filter(is_active=True)
    
    @action(detail=False, methods=['get'], url_path='active-carts')
    def active_carts(self, request):
        """
        Devuelve (o crea) los carritos activos de todos los clientes.
        Si un cliente no tiene carrito activo, se crea automáticamente
        """
        customers = Customer.objects.all()
        active_carts = []

        for customer in customers:
            cart, created = Cart.objects.get_or_create(
                customer=customer,
                is_active=True
            )
            active_carts.append(cart)
        
        serializer = self.get_serializer(active_carts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='current/(?P<customer_id>[^/.]+)')
    def current_cart(self, request, customer_id=None):
        """
        Devuelve (o crea) el carrito activo de un cliente específico.
        """
        cart, created = Cart.objects.get_or_create(
            customer_id=customer_id,
            is_active=True,
        )
        serializer = self.get_serializer(cart)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], url_path='add-item')
    def add_item(self, request, pk=None):
        """
        Agrega o actualiza un producto en el carrito.

        """

        cart = self.get_object()
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        if not product_id:
            return Response({'error': 'Falta product_id'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        

        item, created = cart.items.get_or_create(product=product)
        if quantity <= 0:
            item.delete()
        else:
            item.quantity = quantity
            item.save()

        serializer = self.get_serializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK) 

    @action(detail=True, methods=['post'], url_path='checkout')
    def checkout(self, request, pk=None):
        """
        Convierte un carrito en pedido (checkout).
        """
        cart = self.get_object()
        if not cart.items.exists():
            return Response({'error': 'El carrito está vacío.'}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(
            customer=cart.customer,
            seller=request.user,
            total=cart.get_total(),
        )

        
        for item in cart.items.all():
            order.items.create(
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        
        cart.is_active = False
        cart.save()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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
    
    @action(detail=True, methods=['post'], url_path='update-status')
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')
        if new_status not in ['PENDING', 'PROCESSING', 'COMPLETED', 'CANCELLED']:
            return Response({'error': 'Estado no válido'}, status=status.HTTP_400_BAD_REQUEST)
        order.status = new_status
        order.save()
        serializer = self.get_serializer(order)
        return Response(serializer.data)