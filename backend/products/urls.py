from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import ProductsViewSet


router = SimpleRouter()
router.register("", ProductsViewSet)

urlpatterns = [
    path("", include(router.urls))
]
