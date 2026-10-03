from datetime import date


def calculate_birthday_countdown(birthday: date) -> int:
    """Вернуть количество дней до ближайшего дня рождения."""
    today = date.today()
    next_birthday = get_birthday_for_year(birthday, today.year)

    if next_birthday < today:
        next_birthday = get_birthday_for_year(
            birthday,
            today.year + 1,
        )

    return (next_birthday - today).days


def get_birthday_for_year(birthday: date, year: int) -> date:
    """Вернуть дату дня рождения в указанном году."""
    try:
        return birthday.replace(year=year)
    except ValueError:
        # 29 февраля в невисокосном году считаем 1 марта
        return date(year=year, month=3, day=1)
