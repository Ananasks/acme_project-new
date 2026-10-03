# birthday/validators.py
from datetime import date

from django.core.exceptions import ValidationError


def real_age(value: date) -> None:
    today = date.today()
    age = today.year - value.year

    # Если день рождения в этом году ещё не наступил,
    # полный возраст на единицу меньше
    if (today.month, today.day) < (value.month, value.day):
        age -= 1

    if not 1 <= age <= 120:
        raise ValidationError(
            'Ожидается возраст от 1 года до 120 лет',
        )