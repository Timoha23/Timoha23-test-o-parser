import os
import traceback
import time

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from .exceptions import (
    DivChangesException,
    LastPageException,
    NotFoundProductElementException,
)


user_agent = UserAgent()
URL = "https://www.ozon.ru/seller/1/products"
SOURCE_NAME = "web.html"
PATH = os.path.dirname(os.path.abspath(__file__))
SOURCE_PATH = PATH + "/" + SOURCE_NAME
ITEMS_ON_PAGE = 36

DIV_CLASSES = {
    "card_item": "i9j ik",
    "name": "dx3 x3d d4x yh3 h4y",
    "url": "tile-hover-target yh3 h4y",
    "price": "c3-a1 tsHeadline500Medium c3-b9",
    "discount": "tsBodyControl400Small c3-a2 c3-a7 c3-b1",
    "rating": "u3d",
    "image": "yh7 hy8",
    "limit_page": "uu2",
}


def _load_source_html(
    page_number: int = 1,
    count_loads: int = 0
) -> None:
    """
    Загружаем ресурс с Ozon

    :Args:
      - page_number - страница, которую мы хотим получить
      - count_loads - количество попыток загрузки
    """

    options = Options()
    options.add_argument(f"user-agent={user_agent.random}")
    options.add_argument("-headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    with webdriver.Chrome(options=options) as driver:
        driver.get(f"{URL}/?page={page_number}")
        time.sleep(1)
        with open(SOURCE_PATH, "w") as file:
            file.write(driver.page_source)

    _check_source(
        page_number=page_number,
        load_source_tries=count_loads,
    )


def _check_source(
    page_number: int,
    load_source_tries: int = 0
) -> bool:
    """
    Проверка ресурса.

    Если нет необходимых элементов, скачиваем еще раз (5 попыток),
    если страница последняя - райзим исключение

    :Args:
      - page_number - страница, которую мы хотим получить
      - count_loads - количество попыток загрузки
    """

    with open(SOURCE_PATH, "r") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    items = soup.find_all("div", class_=DIV_CLASSES["card_item"])

    if items == []:
        limit_page = soup.find("div", class_=DIV_CLASSES["limit_page"])

        if limit_page:
            raise LastPageException
        load_source_tries += 1

        if load_source_tries >= 5:
            raise DivChangesException

        _load_source_html(
            page_number=page_number,
            count_loads=load_source_tries,
        )


def _parse_products_from_page_source(
    count_products: int,
    articles_in_database: list[int],
) -> list[dict]:
    """
    Парс ресурса

    :Args:
      - count_products - количество продуктов для парса
      - articles_in_database - список артиклов, которые уже в базе
    (либо уже спаршены в данной задаче)
    """

    current_products_count = 0
    current_products = []

    with open(SOURCE_PATH) as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    products_in_page = soup.find_all("div", class_=DIV_CLASSES["card_item"])

    for product in products_in_page:
        product: BeautifulSoup

        product_template = {
            "name": None,
            "article": None,
            "link": None,
            "price": None,
            "image": None,
            "discount": None,
            "rating": None,
        }

        # Link
        try:
            link = (
                "ozon.ru" +
                product.find("a", class_=DIV_CLASSES["url"])["href"]
            )
        except Exception:
            raise NotFoundProductElementException(
                element="link"
            )

        # Article
        article = link.split("/")[2].split("-")[-1]

        # Check unique or not
        if _binary_search(target=int(article), array=articles_in_database):
            continue

        # Shor link
        short_url = f"ozon.ru/product/{article}/"

        # Name
        try:
            name = product.find("div", class_=DIV_CLASSES["name"]).text
        except Exception:
            raise NotFoundProductElementException(
                element="name"
            )

        # Price
        try:
            price = (
                product
                .find("span", class_=DIV_CLASSES["price"])
                .text
                .replace("\u2009", "")
                .replace("₽", "")
            )
        except Exception:
            raise NotFoundProductElementException(
                element="price"
            )

        # Discount
        try:
            discount = (
                product
                .find("span", class_=DIV_CLASSES["discount"])
                .text[1:-1]
            )
        except Exception:
            discount = None

        # Rating
        try:
            rating = (
                product
                .find("span", class_=DIV_CLASSES["rating"])
                .text.strip()
            )
        except Exception:
            rating = None

        # Image
        try:
            image = (
                product
                .find("div", class_=DIV_CLASSES["image"])
                .find("img")["src"]
            )
        except Exception:
            image = None

        product_template["link"] = short_url
        product_template["price"] = int(price)
        product_template["name"] = name
        product_template["discount"] = int(discount) if discount else None
        product_template["rating"] = float(rating) if rating else None
        product_template["image"] = image
        product_template["article"] = article

        current_products.append(product_template)
        current_products_count += 1

        if count_products == current_products_count:
            break
    return current_products


def _binary_search(target: int, array: list[str]) -> bool:
    """
    Проверка на вхождение продукта в список внесенных продуктов в БД

    :Args:
      - target - продукт
      - array - список продуктов, которые в БД
    """

    left = 0
    right = len(array) - 1

    while left <= right:
        mid = (left + right) // 2
        if array[mid] == target:
            return True
        elif array[mid] > target:
            right = mid - 1
        elif array[mid] < target:
            left = mid + 1
    return False


def _get_products(
    count_products: int,
    articles_in_database: list[int],
) -> list[dict]:
    """
    Получение списка уникальных продуктов после парса

    :Args:
      - count_products - количество продуктов для парса
      - articles_in_database - список артиклов, которые уже в базе
    (либо уже спаршены в данной задаче)
    """

    page_number = 1
    count_products_for_parse = 0
    all_products = []

    while count_products > 0:
        count_products_for_parse = (
            ITEMS_ON_PAGE if count_products >= ITEMS_ON_PAGE
            else count_products
        )

        try:
            _load_source_html(page_number=page_number)
        except LastPageException:
            break
        products = _parse_products_from_page_source(
            count_products=count_products_for_parse,
            articles_in_database=articles_in_database,
        )
        all_products.extend(products)

        articles_in_database.extend(
            int(product["article"]) for product in products
        )
        articles_in_database.sort()

        count_products = count_products - len(products)
        page_number += 1
    return all_products


def get_products(
    count_products: int,
    articles_in_database: list[int],
) -> list[dict]:
    """
    Точка входа. Получение продуктов из магазина Ozon.

    :Args:
      - count_products - количество продуктов для парса
      - articles_in_database - список артиклов, которые уже в базе
    (либо уже спаршены в данной задаче)
    """

    try:
        products = _get_products(
            count_products=count_products,
            articles_in_database=articles_in_database,
        )
        return products
    except DivChangesException as ex:
        return {"error": ex}
    except NotFoundProductElementException as ex:
        return {"error": ex}
    except Exception as ex:
        print(traceback.format_exc())
        return {"error": f"Непредвиденная ошибка {ex}"}
    finally:
        try:
            os.remove(path=SOURCE_PATH)
        except FileNotFoundError:
            pass
