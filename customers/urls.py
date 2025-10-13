from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet

app_name = 'customers'

router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customer')

urlpatterns =router.urls
