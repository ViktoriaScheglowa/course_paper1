import datetime
from pathlib import Path

import pandas as pd
import requests

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
    current_date_time = datetime.datetime.now()
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
    sales_by_card = df_filtered.groupby('Номер карты')['Сумма операции с округлением', 'кэшбек'].sum()
    sorted_sales = sales_by_card.sort_values(by='Сумма операции с округлением', ascending=False)

    print(sorted_sales)
    return sorted_sales


def max_five_transactions(data_time: pd.Timestamp) -> pd.DataFrame:
    """
    Функция, которая извлекает 5 лучших транзакций по сумме платежа.
    """
    df = pd.read_excel(dir_transactions_excel)

    # # Фильтрация транзакций за указанный месяц
    df_filtered = df.loc[
         (pd.to_datetime(df['Дата операции'], dayfirst=True) <= data_time) &
         (pd.to_datetime(df['Дата операции'], dayfirst=True) >= data_time.replace(day=1))
     ]

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
        result = response.json()
        currency_value = result.get('result')

        if currency_value is not None:
            new_currency_list.append(currency_value)
        else:
            print("Ошибка: ключ 'result' не найден в ответе для:", currency)

    return new_currency_list


def price_stocks() -> list:
    """
    Функция, которая извлекает цены акций из списка S&P 500
    путем вызова внешнего API.
    """
    stocks_list = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    price_stock = []

    for stock in stocks_list:
        response = requests.get(f"https://api.twelvedata.com/price?symbol={stock}&apikey={API_KEY_stocks}")
        dict_result = response.json()
        price_element = dict_result.get('price')
        price_stock.append(price_element)

    return price_stock


if __name__ == '__main__':
    print(day_time_now(pd.to_datetime('29-09-2018 00:00:00', dayfirst=True)))
    print(max_five_transactions(pd.to_datetime('29.09.2018', dayfirst=True)))
    print(exchange_rate())
    print(price_stocks())
