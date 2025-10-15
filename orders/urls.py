from rest_framework.routers import DefaultRouter
from .views import CartViewSet, OrderViewSet

app_name = 'orders'

router = DefaultRouter()
router.register(r'carts', CartViewSet, basename='cart')
router.register(r'', OrderViewSet, basename='order')

urlpatterns = router.urls