from rest_framework import serializers

from .models import Product


class GetProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для получения продукта/продуктов
    """

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "article",
            "link",
            "price",
            "discount",
            "rating",
            "image",
        )


class CreateProductSerializer(serializers.Serializer):
    pass


class CreateProductQuerySerializer(serializers.Serializer):
    count = serializers.IntegerField(
        help_text="Количество продуктов для парса",
        default=10
    )
