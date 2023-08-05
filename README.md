# Ozon Parser
## Оглавление
1. [Описание](#описание)
2. [Используемые технологии](#технологии)
3. [Абстрактная схема проекта](#схема)
4. [Запуск](#запуск)
5. [Примеры запросов к API](#примеры_запросов)
6. [Важная информация](#важно)

## Описание
<a name="описание"></a>

Данный проект разработан для парсинга товаров с Ozon, используя REST API с последующим уведомлением в телеграмм об окончании парсинга. Также через телеграмм бота есть возможность получить последний результат парсинга, отправив боту сообщение "Список товаров". В данном проекте для парсинга использован магазин по следующей ссылке - https://www.ozon.ru/seller/1/products/. Перед началом работы настоятельно рекомендую ознакомиться с последним [пунктом](#важно).

<details>
<summary>ТЗ проекта ↓</summary>

Тестовое задание
Разработка парсера товаров сайта Ozon с оповещением


Цели:
 •  Разработка Django приложения.
 •  Создание REST API на основе Django Rest Framework (DRF).
 •  Реализация парсера товаров с сайта Ozon.
 •  Оповещения в Telegram с помощью бота.

Эндпоинты:
 • POST /v1/products/: Запуск задачи на парсинг N товаров. Количество товаров должно приниматься в теле запроса в параметре products_count, по умолчанию 10 (если значение не было передано), максимум 50.
 • GET /v1/products/: Получение списка товаров.
 • GET /v1/products/{product_id}/: Получение товара по айди.
Примеры входных и выходных данных для каждого эндпоинта будут в приложения к тестовому заданию.

Описание проекта:
В рамках этого тестового задания необходимо разработать Django приложение с REST API для парсинга информации о товарах магазина по ссылке с сайта Ozon и сохранения полученных данных о товарах в базу данных. Также требуется настроить оповещения о завершении парсинга через Telegram бота.

Ссылка для парсера:
Парсим по такой ссылке https://www.ozon.ru/seller/1/products/ (именно этот магазин).

Выходные данные:
Для эндпоинта GET /v1/products/: выходными данными будет массив товаров.
Для эндпоинта GET /v1/products/{product_id}/ выходными данными будет один товар.

Требования:
 • Django приложение должно быть разработано с использованием Django Rest Framework.
 • Документирование API должно быть создано с помощью библиотеки Django drf-yasg.
 • Для парсинга данных с сайта Ozon рекомендуется использовать библиотеку BeautifulSoup или другие удобные инструменты.
 • Оповещения должны отправляться в Telegram с помощью Telegram бота.
 • Парсер должен быть реализован с использованием Celery задач.
 • Информация о товарах должна сохраняться в базу данных и отображаться в административной панели.
 • Административная панель должна быть кастомизирована с использованием AdminLTE для современного и привлекательного внешнего вида приложения.

Техническое описание:
 • Версия Python: 3.x
 • Django: 3.x
 • Django Rest Framework: 3.x
 • Celery: 5.x
 • База данных: MySQL

Пример текста для оповещения в Telegram:
Задача на парсинг товаров с сайта Ozon завершена.
Сохранено: N товаров.

Команда для бота: Список товаров
Ожидаемый ответ: бот показывает пронумерованный список товаров последнего парсинга в виде Название + ссылка.

В readme.md должно быть описание то, как запустить проект.
Также в проекте должен быть example.env, если будут использоваться переменные среды. 

Результат задания должен быть выложен в открытый репозиторий на github.
Название репозитория должно быть в формате: “YOURLOGIN-test-o-parser”.


ФОРМАТ ОТКЛИКА: заполнение анкеты, которая вам пришла в ответ на отклик в письме и/или смс.
Ссылка в анкете = ссылка на репозиторий в git для этого задания.
Важно! В корень репозитория положите записанный скринкаст админки со стороны пользователя-админа и просмотр списка товаров в табличном виде.

Срок исполнения — 3 календарных дня (не более 24 ч чистого времени разработки).
</details>

## Используемые технологии
<a name="технологии"></a>

![AppVeyor](https://img.shields.io/badge/Python-3.10.6-green)
![AppVeyor](https://img.shields.io/badge/Django-3.2.20-9cf)
![AppVeyor](https://img.shields.io/badge/djangorestframework-3.14.0-9cf)
![AppVeyor](https://img.shields.io/badge/Selenium-4.10.0-9cf)
![AppVeyor](https://img.shields.io/badge/Beautifulsoup4-4.12.2-9cf)
![AppVeyor](https://img.shields.io/badge/Celery-5.3.1-9cf)
![AppVeyor](https://img.shields.io/badge/aiogram-2.25.1-9cf)

![AppVeyor](https://img.shields.io/badge/Docker-24.0.2-green)
![AppVeyor](https://img.shields.io/badge/docker--compose-1.29.2-9cf)

![AppVeyor](https://img.shields.io/badge/MySQL-8.1.0-green)

![AppVeyor](https://img.shields.io/badge/Redis-7.2-green)

![AppVeyor](https://img.shields.io/badge/Poetry-1.5.1-green)


## Абстрактная схема проекта
<a name="схема"></a>

[![imageup.ru](https://imageup.ru/img189/4458883/my-first-board-2.jpg)](https://imageup.ru/img189/4458883/my-first-board-2.jpg.html)

### Пояснение
В данном проекте существует 1 эндпоинт, способный принять GET-запрос, GET-запрос с path параметром и POST-запрос.

GET-запрос:
```
Когда клиент отправляет GET-запрос на эндпоинт, то REST API(DRF) обращается к базе данных(MySQL), после чего возвращает ответ с необходимыми данными (в зависимости от запроса). Подробный пример запросов представлен ниже в главе "Примеры запросов"
```
POST-запрос:
```
Когда клиент отправляет POST-запрос на эндпоинт, то создается задача (на парсинг магазина), которую исполняет Celery-воркер, после чего данные вносятся в базу данных(MySQL), в Redis добавляется сообщение об успешном выполнении работы парсера, также в Redis добавляется результат последнего парсинга, а именно товары. Телеграмм бот каждые 15 секунд опрашивает Redis на наличие новых уведомлений и если такие имеются, то он отсылает данные уведомления во все чаты, которые указаны в .env в переменной USER_IDS.
```

## Запуск
<a name="запуск"></a>

### Локально
1. Клонируем репозиторий:
   ```bash
   git clone https://github.com/Timoha23/Timoha23-test-o-parser.git
   ```
2. Устанавливаем на систему MySQL и Redis (версии представлены выше), если еще не установлены, либо используем докер образы и разворачиваем в контейнерах.
3. Создаем .env файл и заполняем в соответствии с примером (.env.example).
4. Устанавливаем зависимости:
    ```bash
    poetry install
    ```
5. Переходим в директорию с проектом:
    ```bash
    cd backend/
    ```
6. Создаем миграции:
   ```bash
   python manage.py makemigrations
   ```
7. Накатываем миграции:
   ```bash
   python manage.py migrate
   ```
8. Собираем статику:
   ```bash
   python manage.py collectstatic
   ```
9. Запускаем REST API сервис:
   ```bash
   python manage.py runserver
   ```
10. В новом терминале переходим в директорию, что и на шаге 5 и запускаем Celery:
    ```bash
    celery -A backend worker --concurrency=1 -l info
    ```
11. В новом терминале из корня проекта переходим в директорию с ботом:
    ```bash
    cd bot/
    ```
12. Запускаем бота:
    ```bash
    python main.py
    ```

###  Докер
1. Клонируем репозиторий:
   ```bash
   git clone https://github.com/Timoha23/Timoha23-test-o-parser.git
   ```

2. Создаем .env файл и заполняем в соответствии с примером (.env.example).
3. Поднимаем контейнеры:
   ```bash
   docker-compose up -d --build
   ```
4. Создание администратора:
   ```bash
   docker-compose exec backend bash
   
   # После чего вы можете использовать консоль данного контейнера. Далее все стандартно: python manage.py createsuperuser
   ```

## Примеры запросов к API
<a name="примеры_запросов"></a>

1. Получение товаров из базы данных
   * Endpoint: **host:port/api/v1/products/**
   * Method: **GET**
   * Response:
      ```json
      [
        {
          "id": 0,
          "name": "string",
          "article": 2147483647,
          "link": "string",
          "price": 2147483647,
          "discount": 2147483647,
          "rating": 0,
          "image": "string"
        }
      ]
      ``` 
   * Postman
      <details>
     <summary>Спойлер</summary>
      
     [![Пример запроса][1]][1]
      
     [1]: https://imageup.ru/img278/4458921/ozon-get.png
     </details>

2. Получение товара по id из базы данных
   * Endpoint: **host:port/api/v1/products/{id}/**
   * Method: **GET**
   * Params:
    * Path
      ```json
      {
        "id": 0
      }
      ```
   * Response:
      ```json
      {
        "id": 0,
        "name": "string",
        "article": 2147483647,
        "link": "string",
        "price": 2147483647,
        "discount": 2147483647,
        "rating": 0,
        "image": "string"
      }
      ``` 
   * Postman
      <details>
     <summary>Спойлер</summary>
      
     [![Пример запроса][2]][2]
      
     [2]: https://imageup.ru/img159/4458930/ozon-get-1.png
     </details>  

3. Запрос на парсинг товаров с последующим занесением в БД.
   * Endpoint: **host:port/api/v1/products/**
   * Method: **POST**
   * Params:
    * Query
      ```json
      {
        "count": 10
      }
      ```
  
   * Response:
      ```json
      {}
      ``` 
   * Postman
      <details>
     <summary>Спойлер</summary>
      
     [![Пример запроса][3]][3]
      
     [3]: https://imageup.ru/img200/4458935/ozon-post.png
     </details>

## Примеры взаимодействия с телеграмм ботом
<a name="бот"></a>

1. Для получения списка последних спаршенных товаров отправляем боту следующее сообщение: "Список товаров" в ответ получаем следующее сообщение:
   <details>
   <summary>Скриншот</summary>

   [![Пример запроса][4]][4]

   [4]: https://imageup.ru/img93/4460553/bot_product_list.jpg
   </details>

2. Пример уведомления после окончания парсинга:
   <details>
   <summary>Скриншот</summary>

   [![Пример запроса][5]][5]

   [5]: https://imageup.ru/img262/4460555/notification_from_bot.jpg
   </details>



## Важная информация
<a name="важно"></a>

1. Для того, чтобы бот смог отправлять вам уведомление первоначально необходимо отправить боту /start, чтобы он мог отправлять вам уведомления, далее внести свой id в файл .env в переменную USER_IDS. Можно внести несколько id, но нужно это сделать через запятую.
2. Так как ozon с определенной переодичностью изменяет название у классов div и других элементов, то есть необходимость обновлять данные классы в ручную в файле backend/backend/parser/ozon_parser.py в словаре DIV_CLASSES. Откуда брать новые названия классов прилагаю ниже:
    <details>
    <summary>Названия классов ↓</summary>
    
    1. card_item
    [![][6]][6]

    [6]: https://imageup.ru/img228/4458955/card_item.jpg

    2. name
    [![][7]][7]
    
    [7]: https://imageup.ru/img207/4458957/name.jpg
    

    3. url
    [![][8]][8]
    
    [8]: https://imageup.ru/img204/4458960/url.jpg
    
    
    4. price
    [![][9]][9]
    
    [9]: https://imageup.ru/img26/4458961/price.jpg
    

    5. discount
    [![][10]][10]
    
    [10]: https://imageup.ru/img227/4458963/discount.jpg
    

    6. rating
    [![][11]][11]
    
    [11]: https://imageup.ru/img266/4458965/rating.jpg
    

    7. image
    [![][12]][12]
    
    [12]: https://imageup.ru/img213/4458966/image.jpg

    8. limit_page
    [![][13]][13]
    
    [13]: https://imageup.ru/img268/4458976/limit_page.png
    </details>