DATE_DICT = {
    "1": "января", "2": "февраля",
    "3": "марта", "4": "апреля",
    "5": "мая", "6": "июня",
    "7": "июля", "8": "августа",
    "9": "сентября", "10": "октября",
    "11": "ноября", "12": "декабря",
}

LOG_INFORMATION = "INFO"
LOG_WARNING = "WARN"
LOG_ERROR = "ERR"

PRIORITY_LOW = 0
PRIORITY_NORMAL = 1
PRIORITY_MEDIUM = 2
PRIORITY_HIGH = 3
PRIORITIES_LIST = {
    "Обычный": 0,
    "Низкий": 1,
    "Средний": 2,
    "Высокий": 3
}

PRIORITIES_LIST2 = {
    0: "Обычный",
    1: "Низкий",
    2: "Средний",
    3: "Высокий"
}

DEBT_SORT_DEFAULT = 0
DEBT_SORT_DEBTOR = 1
DEBT_SORT_AMOUNT = 2
DEBT_SORT_DATE = 3
DEBT_SORT_LIST = {
    "По новизне": 0,
    "По алфавиту(должник)": 1,
    "По сумме": 2,
    "По дате": 3,
    "По приоритету": 4,
}

DEBT_SEARCH_LIST = {
    "Все столбцы": 0,
    "ID": 1,
    "Приоритет": 2,
    "Задолжник": 3,
    "Сумма": 4,
    "Описание": 5,
    "Дата": 6,
}
