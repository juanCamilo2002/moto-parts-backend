from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Product, Category, Brand
from .serializers import ProductSerializer, CategorySerializer, BrandSerializer
from .permissions import IsAuthenticatedReadAndAdminWrite

@extend_schema(tags=["Catálogo"], summary="Gestión de categorías")
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedReadAndAdminWrite, )


@extend_schema(tags=["Catálogo"], summary="Gestión de marcas")
class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = (IsAuthenticatedReadAndAdminWrite, )


@extend_schema(
    tags=["Catálogo"],
    summary="Gestionar productos del catálogo",
    description="Permite listar, crear, actualizar y eliminar productos del catálogo. Solo los administradores pueden modificar datos.",
)
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticatedReadAndAdminWrite, )

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)