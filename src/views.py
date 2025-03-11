import json
import os

import pandas as pd
import datetime

from dotenv import load_dotenv
from pathlib import Path

from src.utils import get_currency_rates, get_data_range, get_stock_prices, group_expenses, group_income
from src.utils import (day_time_now, exchange_rate, price_stocks, max_five_transactions, user_transactions)
from typing import Union
from config import file_path, file_path1

load_dotenv('../.env')


# Определение текущего каталога
current_dir = Path(__file__).parent.parent.resolve()
dir_transactions_excel = current_dir/'data'/'operations.xlsx'
print(dir_transactions_excel)


def website(data_time: datetime) -> Union[list, dict]:

    """ Главная функция, принимающую на вход строку с датой и временем в формате
    YYYY-MM-DD HH:MM:SS и возвращающую JSON-ответ: """


    print(f"Входные данные: {data_time}")
    result1 = day_time_now()  #Приветствие в формате текущего времени.
    result2 = user_transactions(data_time)  #Транзакции по картам
    result3 = max_five_transactions(data_time)  #Топ-5 транзакций по сумме платежа.
    result4 = exchange_rate()  #Курс валют.
    result5 = price_stocks() #Стоимость акций из S&P500.

    return result1, result2, result3, result4, result5


if __name__ == '__main__':

    print(f'{day_time_now()}')
    print(user_transactions(pd.to_datetime('29-09-2018 00:00:00', dayfirst=True)))
    data_time = pd.Timestamp("29-09-2018 00:00:00")  # Пример даты
    result = user_transactions(data_time)
    print("Результат транзакций:")
    print(result)
    print("Пять максимальных транзакций:")

def analyze_data(date_str, data_range="M"):
    """Главная функция для анализа данных."""
    start_date, end_date = get_data_range(date_str, data_range)
    filtered_data = pd.read_excel(file_path)
    filtered_data["Дата операции"] = filtered_data["Дата операции"].astype(str).str.strip()

    try:
        # Преобразуем 'Дата операции' в формат даты и времени
        filtered_data["Дата операции"] = pd.to_datetime(filtered_data["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    except Exception as e:
        print(f"Ошибка при преобразовании дат: {e}")

    # Фильтруем данные по дате
    filtered_data = filtered_data[
        (filtered_data["Дата операции"] >= start_date) & (filtered_data["Дата операции"] <= end_date)
    ]
    # Анализ расходов
    expenses_summary = group_expenses(filtered_data)
    total_expenses = filtered_data["Сумма операции"].sum()
    # Анализ поступлений
    income_summary = group_income(filtered_data)
    total_income = filtered_data["Сумма операции"][filtered_data["Сумма операции"] > 0].sum()
    # Получение валютных курсов и цен акций
    try:
        with open(file_path1) as f:
            user_settings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise ValueError(f"Ошибка при чтении файла настроек пользователя: {e}")

    currency_rates = get_currency_rates(user_settings["user_currencies"])
    stock_prices = get_stock_prices(user_settings["user_stocks"])
    # Формирование итогового ответа
    result = {
        "Расходы": {"Общая сумма": total_expenses, "Основные": expenses_summary.to_dict(orient="records")},
        "Поступления": {"Общая сумма": total_income, "Основные": income_summary.to_dict(orient="records")},
        "Курс валют": currency_rates,
        "Цены акций": stock_prices,
    }
    return result


# Пример вызова функции анализа данных к веб-странице События
result = analyze_data(date_str="31.12.2021 16:44:00", data_range="M")
print(json.dumps(result, ensure_ascii=False, indent=4))