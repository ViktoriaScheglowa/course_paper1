import json
import logging
from collections import defaultdict
from datetime import datetime
from functools import reduce

import pandas as pd

logger = logging.getLogger(__name__)


def get_beneficial_cashback_categories(data, year, month):
    """
    Функция «Выгодные категории повышенного кешбэка»
    Фильтрует транзакции по указанному году и месяцу

    Параметры:
        data: pd.DataFrame - DataFrame с транзакциями
        year: int - Год для фильтрации
        month: int - Месяц для фильтрации (1-12)
    """

    logger.info("Анализ категорий кешбэка за %d-%02d", year, month)
    if not isinstance(data, pd.DataFrame):
        raise ValueError("Требуется pandas DataFrame")

    data['date'] = pd.to_datetime(data['Дата операции'], dayfirst=True)

    # Функция для фильтрации транзакций по году и месяцу
    filtered = data[(data['date'].dt.year == year) & (data['date'].dt.month == month)].copy()
    if not filtered.empty:
        cashback = (filtered.groupby('Категория')['Сумма операции с округлением']
                    .sum()
                    .div(100)
                    .round()
                    .astype(int)
                    .to_dict())
    else:
        cashback = {}


    # Функция для аккумулирования сумм по категориям
    def accumulate(acc, transaction):
        category = transaction["category"]
        amount = abs(transaction["amount"])
        acc[category] += amount
        return acc

    category_cashback = reduce(accumulate, filtered, defaultdict(int))

    # Формируем кэшбэк (1% от суммы) и превращаем его в обычный словарь
    cashbacks = {category: round(amount * 0.01) for category, amount in category_cashback.items()}

    return json.dumps(cashbacks, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    print(json.dumps)
