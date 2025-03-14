from src.utils import (day_time_now, exchange_rate, price_stocks, max_five_transactions, user_transactions)
from typing import Union
import pandas as pd
import datetime
from pathlib import Path


current_dir = Path(__file__).parent.parent.resolve()

dir_transactions_excel = current_dir/'data'/'operations.xlsx'
print(dir_transactions_excel)


def website(data_time: datetime) -> Union[list, dict]:
    """ Главная функция, принимающую на вход строку с датой и временем в формате
    YYYY-MM-DD HH:MM:SS и возвращающую JSON-ответ: """
    print(f"Входные данные: {data_time}")
    result_time = day_time_now()
    result_transactions = user_transactions(data_time)
    result_top = max_five_transactions(data_time)
    result_exchange = exchange_rate()
    result_price = price_stocks()

    return [result_time, result_transactions, result_top, result_exchange, result_price]


if __name__ == '__main__':

    print(f'{day_time_now()}')
    print(user_transactions(pd.to_datetime('29-09-2018 00:00:00', dayfirst=True)))
    data_time = pd.Timestamp("29-09-2018 00:00:00")
    result = user_transactions(data_time)
    print("Результат транзакций:")
    print(result)
    print("Пять максимальных транзакций:")
