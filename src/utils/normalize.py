import datetime
import re


import parsedatetime
from dateutil.relativedelta import relativedelta

constants = parsedatetime.Constants(localeID='ru_RU', usePyICU=False)
calendar = parsedatetime.Calendar(constants)


UNITS = {
    'days': ['день', 'дней', 'дня', 'д'],
    'weeks': ['неделя', 'недели', 'недель', 'н'],
    'months': ['месяц', 'месяца', 'мес'],
    'years': ['год', 'года', 'годы', 'г'],
    'halfyear': ['полгода'],
}

NUMBERS = {
    'одного': 1,
    'одной': 1,
    'два': 2,
    'двух': 2,
    'три': 3,
    'трех': 3,
    'трёх': 3,
    'четыре': 4,
    'пять': 5,
    'шесть': 6,
    'семь': 7,
    'восемь': 8,
    'девять': 9,
    'десять': 10,
    'одиннадцать': 11,
    'двенадцать': 12,
    'тринадцать': 13,
    'четырнадцать': 14,
    'пятнадцать': 15,
    'шестнадцать': 16,
    'семнадцать': 17,
    'восемнадцать': 18,
    'девятнадцать': 19,
    'двадцать': 20,
}


def get_date(datestring: str):
    cutted = re.sub(r'^\D+|\D+$', '', datestring)
    result, code = calendar.parse(cutted)
    if not code:
        raise ValueError(
            f"Не удалось определить формат времени в строке {datestring}"
        )
    return datetime.datetime(*result[:3])


def normalize_date(date: datetime.datetime):
    return f"{date.year}_{date.month}_{(date.day - 1) // 7 + 1}_{date.day}"


def format_date(
        date: datetime.datetime
):
    return f"{date.year}_{date.month}_{(date.day - 1) // 7 + 1}_{date.day}"


def parse_raw(raw: str):
    words = raw.lower().split()
    for index, word in enumerate(words):
        if word.isnumeric():
            offset = int(word)
            for key in UNITS.keys():
                if words[index + 1] in UNITS[key]:
                    return {key: offset}

    for index, word in enumerate(words):
        if word in NUMBERS.keys():
            offset = NUMBERS[word]
            for key in UNITS.keys():
                if words[index + 1] in UNITS[key]:
                    return {key: offset}

    for index, word in enumerate(words):
        for key in UNITS.keys():
            if word in UNITS[key]:

                if key == 'halfyear':
                    return {'months': 6}

                return {key: 1}

    raise ValueError(f"Не удалось преобразовать данные в {raw}")


def get_deadline_date(order_date: datetime.datetime, deadline: str):
    return order_date + relativedelta(**parse_raw(deadline))
