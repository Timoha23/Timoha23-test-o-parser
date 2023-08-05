from django.db import models


class Product(models.Model):
    """
    Модель продукта
    """

    name = models.CharField(
        max_length=1024,
        verbose_name="Название",
    )
    link = models.CharField(
        max_length=1024,
        verbose_name="Ссылка",
    )
    article = models.IntegerField(
        verbose_name="Артикл",
    )
    price = models.IntegerField(
        verbose_name="Цена",
    )
    discount = models.IntegerField(
        verbose_name="Скидка",
        blank=True,
        null=True,
    )
    rating = models.FloatField(
        verbose_name="Рейтинг",
        blank=True,
        null=True,
    )
    image = models.CharField(
        max_length=1024,
        verbose_name="Картинка",
        blank=True,
        null=True,
    )
    updated_date = models.DateTimeField(
        verbose_name="Дата обновления",
        auto_now=True,
    )
    created_date = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return self.name[:29] + "..." if len(self.name) > 32 else self.name
