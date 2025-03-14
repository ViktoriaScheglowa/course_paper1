from typing import Any
import pandas as pd

from src.reports import dir_transactions_excel, spending_by_category
from src.services import get_beneficial_cashback_categories
from src.views import website


def main() -> Any:
    """Функция для запуска всего проекта"""
    print("Функция для запуска всего проекта")


if __name__ == '__main__':
    print("\nГЛАВНАЯ\n")

    data_time = pd.Timestamp("29-09-2018 00:00:00")
    result_time, result_transactions, result_top, result_exchange, result_price = website(data_time)
    # print("После вызова website")
    print(result_time, result_transactions, result_top, result_exchange, result_price)

    print("\nСервисы.Выгодные категории повышенного кешбека\n")
    get_beneficial_cashback_categories(data, year, month)

    print("\nОТЧЕТЫ\n")
    spending_by_category(pd.read_excel(dir_transactions_excel), 'Переводы', '23.08.2018')
