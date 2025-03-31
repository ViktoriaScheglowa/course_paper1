import pandas as pd
import pytest

from src.reports import spending_by_category

transactions_data = {
    'Категория': ['Фастфуд', 'Фастфуд', 'Развлечения'],
    'Дата операции': ['10.11.2019', '12.11.2019', '15.11.2019'],
    'Сумма': [100, 150, 200]
}
transactions_df = pd.DataFrame(transactions_data)


# Тест функции
@pytest.mark.parametrize("category, date, expected_count", [
    ('Фастфуд', '11.11.2019', 98),
    ('Фастфуд', None, 0),  # Проверка с текущей датой
    ('Развлечения', '11.11.2019', 0),
])
def test_spending_by_category(category, date, expected_count):
    result = spending_by_category(transactions_df, category, date)
    assert len(result) == expected_count
