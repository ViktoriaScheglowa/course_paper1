import json
import datetime
import logging
import pandas as pd
import requests

from datetime import datetime, timedelta
from pathlib import Path
from config import API_KEY_exchange, API_KEY_stocks


# Определение текущего каталога
current_dir = Path(__file__).parent.parent.resolve()
dir_transactions_excel = current_dir / 'data' / 'operations.xlsx'
print(dir_transactions_excel)


def day_time_now():
    """
    Функция, которая приветствует в зависимости от текущего времени суток.
    Возвращает строку приветствия в зависимости от времени.
    """
    current_date_time = datetime.datetime.now()  #текущее время
    hour = current_date_time.hour

    if 0 <= hour < 6 or 22 <= hour <= 23:
        return "Доброй ночи"
    elif 17 <= hour <= 22:
        return "Добрый вечер"
    elif 7 <= hour <= 11:
        return "Доброе утро"
    else:
        return "Добрый день"


def user_transactions(data_time: pd.Timestamp) -> pd.DataFrame:
    """
    Функция, которая извлекает детали транзакций для каждой карты:
    - последние 4 цифры карты
    - общие расходы
    - кэшбек (1 рубль за каждые 100 рублей расхода)
    """
    df = pd.read_excel(dir_transactions_excel)

    # Фильтрация транзакций за указанный месяц
    df_filtered = df.loc[
         (pd.to_datetime(df['Дата операции'], dayfirst=True) <= data_time) &
         (pd.to_datetime(df['Дата операции'], dayfirst=True) >= data_time.replace(day=1))
     ]

    # Расчет кэшбека и группировка по номеру карты
    df_filtered.loc[:, 'кэшбек'] = df_filtered['Сумма операции с округлением'] // 100
    sales_by_card = df_filtered.groupby('Номер карты')[['Сумма операции с округлением', 'кэшбек']].sum()
    sorted_sales = sales_by_card.sort_values(by='Сумма операции с округлением', ascending=False)

    print(sorted_sales)
    return sorted_sales


def max_five_transactions(data_time: pd.Timestamp) -> pd.DataFrame:
    """
    Функция, которая извлекает 5 лучших транзакций по сумме платежа.
    """
    df = pd.read_excel(dir_transactions_excel)

    # # Фильтрация транзакций за указанный месяц
    # df_filtered = df.loc[
    #     (pd.to_datetime(df['Дата операции'], dayfirst=True) <= data_time) &
    #     (pd.to_datetime(df['Дата операции'], dayfirst=True) >= data_time.replace(day=1))
    # ]
    # Создаем копию для фильтрации
    filtered_df = df.copy()

    # Фильтрация транзакций за указанный месяц
    filtered_df = filtered_df.loc[
        (pd.to_datetime(filtered_df['Дата операции'],
                        format="%d.%m.%Y %H:%M:%S", dayfirst=True) <= data_time) &
        (pd.to_datetime(filtered_df['Дата операции'],
                        format="%d.%m.%Y %H:%M:%S", dayfirst=True) >= data_time.replace(day=1))
        ]
    # Сортировка и получение 5 лучших транзакций
    top_transactions = filtered_df.sort_values(by='Сумма операции с округлением', ascending=False).head(5)
    return top_transactions


def exchange_rate() -> list:
    """
    Функция, которая извлекает курсы обмена для USD и EUR к RUB
    путем вызова внешнего API.
    """
    currency_list = ["USD", "EUR"]
    convert_to = "RUB"
    new_currency_list = []

    for currency in currency_list:
        url = f"https://api.apilayer.com/currency_data/convert"
        headers = {"apikey": API_KEY_exchange}

        response = requests.get(url, headers=headers)
        # print("Response:", response.text)  # Отладочный вывод
        result = response.json()
        currency_value = result.get('result')

        if currency_value is not None:
            new_currency_list.append(currency_value)
        else:
            print("Ошибка: ключ 'result' не найден в ответе для:", currency)

    return new_currency_list


def get_price_stocks_snp500() -> list:
    """
    Функция, которая извлекает цены акций из списка S&P 500
    путем вызова внешнего API.
    """
    stocks_list = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    price_stocks = []

    for stock in stocks_list:
        response = requests.get(f"https://api.twelvedata.com/price?symbol={stock}&apikey={API_KEY_stocks}")
        dict_result = response.json()
        price_element = dict_result.get('price')
        price_stocks.append(price_element)

    return price_stocks


if __name__ == '__main__':
    print(day_time_now())
    print(user_transactions(pd.to_datetime('29-09-2018 00:00:00', dayfirst=True)))
    print(max_five_transactions(pd.to_datetime('29.09.2018', dayfirst=True)))
    print(exchange_rate())
    print(get_price_stocks_snp500())

# Настройка логирования
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")


def get_data_range(date_str, data_range):
    # Преобразуйте входную строку на случай, если время отсутствует
    if len(date_str) == 10:  # формат 'DD.MM.YYYY'
        date_str += " 00:00:00"
        logging.debug(f"Преобразована строка даты: {date_str}")

    # Теперь можно безопасно разбирать строку
    parsed_date = datetime.strptime(date_str, "%d.%m.%Y %H:%M:%S")
    logging.debug(f"Разобранная дата: {parsed_date}")

    if data_range == "M":
        start_date = parsed_date.replace(hour=0, minute=0, second=0)
        end_date = (start_date + timedelta(days=31)).replace(day=1) - timedelta(seconds=1)
        end_date = end_date.replace(hour=23, minute=59, second=59)
        logging.debug(f"Месячный период: {start_date} - {end_date}")

    elif data_range == "W":
        start_date = parsed_date - timedelta(days=parsed_date.weekday())  # Понедельник
        end_date = start_date + timedelta(days=6)  # Воскресенье
        end_date = end_date.replace(hour=23, minute=59, second=59)
        logging.debug(f"Недельный период: {start_date} - {end_date}")

    elif data_range == "Y":
        start_date = parsed_date.replace(month=1, day=1, hour=0, minute=0, second=0)
        end_date = parsed_date.replace(month=12, day=31, hour=23, minute=59, second=59)
        logging.debug(f"Годовой диапазон: {start_date} - {end_date}")

    elif data_range == "ALL":
        # Логика для ALL
        start_date = datetime(2021, 1, 1, 16, 44, 0)
        end_date = parsed_date
        logging.debug(f"Период даты и времени: {start_date} - {end_date}")

    else:
        logging.error("Недопустимый период")
        raise ValueError("Invalid period")

    return start_date, end_date


def get_currency_rates(currencies):
    rates = {}
    for currency in currencies:
        logging.debug(f"Запрос курсов для валюты: {currency}")
        try:
            response = requests.get(
                f"https://v6.exchangerate-api.com/v6/ed5608baba940bd1aa75173b/latest/USD {currency}"
            )
            response.raise_for_status()
            rates[currency] = response.json().get("rates", {})
            logging.info(f"Успешно получены курсы для {currency}: {rates[currency]}")
        except requests.RequestException as e:
            logging.error(f"Ошибка при получении курса для {currency}: {e}")
            rates[currency] = {}
    return rates


def get_stock_prices(stocks):
    """Получает цены акций."""
    prices = {}
    for stock in stocks:
        logging.debug(f"Запрос цены для акции: {stock}")
        try:
            response = requests.get(
                f"https://api.marketstack.com/v1/eod?access_key=df3caee3a4eb8c55e2af01775ca399c8&symbols=AAPL {stock}"
            )
            response.raise_for_status()  # Проверка на ошибки HTTP
            prices[stock] = response.json().get("price", None)
            logging.info(f"Успешно получена цена для {stock}: {prices[stock]}")
        except requests.RequestException as e:
            logging.error(f"Ошибка при получении цены для {stock}: {e}")
            prices[stock] = None
    return prices


def group_expenses(filtered_data):
    """Группирует расходы по категориям и возвращает основные категории."""
    logging.debug("Начало группировки расходов")
    expenses_by_category = (
        filtered_data[filtered_data["Сумма операции"] < 0].groupby("Категория")["Сумма операции"].sum().reset_index()
    )
    expenses_by_category["Сумма операции"] = expenses_by_category["Сумма операции"].round(0)
    top_expenses = expenses_by_category.nlargest(7, "Сумма операции")
    other_expenses_sum = expenses_by_category.loc[
        ~expenses_by_category["Категория"].isin(top_expenses["Категория"]), "Сумма операции"
    ].sum()

    other_expenses = pd.DataFrame({"Категория": ["Остальное"], "Сумма операции": [other_expenses_sum]})
    combined_expenses = pd.concat([top_expenses, other_expenses], ignore_index=True)

    logging.info("Группировка расходов завершена")
    return combined_expenses


def group_income(filtered_data):
    """Группирует поступления по категориям и возвращает основные категории."""
    logging.debug("Начало группировки поступлений")
    income_by_category = (
        filtered_data[filtered_data["Сумма операции"] > 0].groupby("Категория")["Сумма операции"].sum().reset_index()
    )
    income_by_category["Сумма операции"] = income_by_category["Сумма операции"].round(0)
    top_income = income_by_category.nlargest(7, "Сумма операции")
    other_income_sum = income_by_category.loc[
        ~income_by_category["Категория"].isin(top_income["Категория"]), "Сумма операции"
    ].sum()
    other_income = pd.DataFrame({"Категория": ["Остальное"], "Сумма операции": [other_income_sum]})
    combined_income = pd.concat([top_income, other_income], ignore_index=True)

    logging.info("Группировка поступлений завершена")
    return combined_income