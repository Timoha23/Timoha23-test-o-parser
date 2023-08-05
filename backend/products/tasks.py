import json
from datetime import datetime, timezone
from backend.parser.ozon_parser import get_products

from backend.cache import cache
from backend.celery import app

from .models import Product


@app.task
def create_products(
    count: int,
):
    """
    Таск на внесение продуктов в БД

    :Args:
      - count - количество продуктов
    """

    start_time = datetime.now(timezone.utc).replace(microsecond=0)

    products_from_db = Product.objects.all().order_by("article")
    not_unique_products_articles = [product.article for product in
                                    products_from_db]

    products = get_products(
        count_products=count,
        articles_in_database=not_unique_products_articles,
    )

    error = _have_errors(products)

    if error:
        message = str(error)
        cache.rpush("notification", message)
        return

    Product.objects.bulk_create([Product(**product) for product in products])

    end_time = datetime.now(timezone.utc).replace(microsecond=0)
    duration_time = end_time - start_time

    message = (
        "Задача на парсинг товаров с сайта Ozon завершена.\n"
        f"Сохранено: {len(products)} товаров.\n"
        f"Время начала: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"Время окончания: {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"Продолжительность: {duration_time}\n\n"
        "Время указано в UTC."
    )

    cache.rpush("notification", message)

    products_dict = {
        i+1: (product["name"], product["link"]) for i, product
        in enumerate(products)
    }
    dct_str = json.dumps(products_dict)
    cache.set("last_parse", dct_str)


def _have_errors(products: list[dict] | dict) -> str | None:
    """
    Проверка на ошибки

    :Args:
      - products - список продуктов.
    """

    if isinstance(products, dict):
        error = products.get("error")
        return error
    return
