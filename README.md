# # Проект "course_paper1"

## Описание:

Приложение для анализа транзакций, которые находятся в Excel-файле.

## Установка:

1. Клонируйте репозиторий:
```
git clone https://github.com/ViktoriaScheglowa/projecthome.git
```

2. Установите зависимости:
```
pip install -r requirements.txt
```

3. Создайте базу данных и выполните миграции:
```
python manage.py migrate
```

4. Запустите локальный сервер:
```
python manage.py runserver
```
## Используемые функции:

1. Главная функция, принимающую на вход строку с датой и временем в формате
    YYYY-MM-DD HH:MM:SS и возвращающую JSON-ответ.
2. Главная функция для анализа данных.
3. Функция, которая приветствует в зависимости от текущего времени суток.
    Возвращает строку приветствия в зависимости от времени.
4. Функция, которая извлекает детали транзакций для каждой карты.
5. Функция, которая извлекает 5 лучших транзакций по сумме платежа.
6. Функция, которая извлекает курсы обмена для USD и EUR к RUB
    путем вызова внешнего API.
7. Функция, которая извлекает цены акций из списка S&P 500
    путем вызова внешнего API.
8. Функция преобразующая входную строку в диапазон дат.
9. Функция получающая курс валют.
10. Функция получающая цены акций.
11. Функция группирующая расходы по категориям и возвращает основные категории.
12. Функция группирующая поступления по категориям и возвращает основные категории.
13. Функция «Выгодные категории повышенного кешбэка».
14. Функция возвращает траты по заданной категории за последние три месяца


## Тестирование:

Для запуска тестирования необходимо в терминале ввести "pytest"

## Документация:

Дополнительную информацию о структуре проекта и API можно найти в [документации](docs/README.md).

## Лицензия:

Проект распространяется под [лицензией MIT](LICENSE).
