from datetime import datetime

from src.views import website


def test_website1():
    """Тестирование правильности работы функции"""
    data_time = datetime.now()
    result = website(data_time)

    # Проверка, что результат имеет ожидаемый тип и значения
    assert isinstance(result, tuple)
    assert len(result) == 5
    assert isinstance(result[0], str)
