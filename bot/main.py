import asyncio
import json
import os

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

from bot.cache import cache


load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")

USER_IDS = os.getenv("USER_IDS").split(",")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot=bot)


async def _send_message(message: str):
    for user_id in USER_IDS:
        try:
            await bot.send_message(chat_id=user_id, text=message)
        except Exception as ex:
            print("Exception = ", ex)


async def polling_telegram_notification():
    """
    Запуск цикла на проверку уведомлений о результате парса
    """

    while True:
        while cache.lrange("notification", 0, -1):
            notify = cache.lpop("notification")
            await _send_message(message=notify)
        await asyncio.sleep(15)


@dp.message_handler(text="Список товаров")
async def send_products(message: types.Message):
    """
    Получение списка последних спаршенных товаров
    """

    last_parse = cache.get("last_parse")

    if last_parse is None:
        await message.answer("Нет информации о последнем парсе")
    else:
        last_parse = json.loads(cache.get("last_parse"))

        products = ""
        counter = 1
        products_list = [(value[0], value[1]) for value in last_parse.values()]
        while products_list:
            product = products_list.pop(0)
            new_product = f"{counter}. {product[0]}. Ссылка {product[1]}\n"
            if len(products) + len(new_product) > 4050:
                products_list.insert(0, product)
                await message.answer(products)
                products = ""
                continue
            products += new_product
            counter += 1
        await message.answer(products)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(polling_telegram_notification())
    executor.start_polling(dp, skip_updates=True)
