from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Product
from .serializers import (
    CreateProductQuerySerializer,
    CreateProductSerializer,
    GetProductSerializer
)
from .tasks import create_products


class ProductsViewSet(viewsets.ModelViewSet):
    """
    Обработчик создания/получения товара
    """

    queryset = Product.objects.all().order_by("name")
    http_method_names = ["get", "post"]

    def get_serializer_class(self):
        if self.action == "create":
            return CreateProductSerializer
        return GetProductSerializer

    @swagger_auto_schema(
        query_serializer=CreateProductQuerySerializer,
    )
    def create(self, request):
        count = request.query_params.get("count")
        if count.isdigit():
            count = int(count)
            if count < 10 or count > 50:
                return Response(
                    data={"error": "Количество может быть от 10 до 50"},
                    status=400,
                )
        else:
            return Response(
                    data={"error": "Количество - это число"},
                    status=400,
                )
        create_products.delay(
            count=count,
        )

        return Response(status=201)
