from rest_framework.routers import DefaultRouter
from .views import ProductViewSet

app_name = 'catalog'
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns =  router.urls