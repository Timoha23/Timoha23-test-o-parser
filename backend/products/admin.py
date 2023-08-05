from django.contrib import admin

from .models import Product


class ProductAdminConfig(admin.ModelAdmin):

    list_display = (
        "name",
        "article",
        "link",
        "price",
        "discount",
        "rating",
        "image",
        "updated_date",
        "created_date",
    )
    search_fields = ("name",)


admin.site.register(Product, ProductAdminConfig)
