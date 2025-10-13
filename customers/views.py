from rest_framework import viewsets, permissions
from drf_spectacular.utils import extend_schema
from .models import Customer
from .serializers import CustomerSerializer

@extend_schema(
    tags=['Clientes'],
    summary='Gestión de clientes',
    description='Permite listar, crear, actualizar y eliminar clientes'
)
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by('-created_at')
    serializer_class = CustomerSerializer
    permission_classes = (permissions.IsAuthenticated, )

  