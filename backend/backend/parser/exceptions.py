class DivChangesException(Exception):

    def __str__(self) -> str:
        return (
            "Ошибка: сравните имена классов для блочных элементов. "
            "Задача на парсинг товаров с сайта Ozon не завершена."
        )


class LastPageException(Exception):

    def __str__(self) -> str:
        return (
            "Ошибка: новых товаров в магазине не найдено. "
            "Спаршено 0 товаров."
        )


class NotFoundProductElementException(Exception):

    def __init__(self, element: str):
        self.element = element
        super().__init__()

    def __str__(self) -> str:
        return f"Не найден ключевой элемент {self.element} для товара"
