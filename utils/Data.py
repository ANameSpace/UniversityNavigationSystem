from PySide6.QtGui import QColor

from utils.tools.Log import Log

walls = [
    (0, 0, 0, 40),
    (0, 40, 40, 40)
]

ladders = [
    ("l1", 0, 25, 10, 10),
    ("l2", 0, 80, 50, 60)
]

erooms = [
    (0, 0, 1, 2),
    (-10, 1, 8, 5)
]

rooms = [
    ("1.1", 3, 1, 10, 12, QColor(0, 10, 10)),
    ("1.2", 1, 15, 8, 5, QColor(0, 100, 100)),
    ("1.3", 1, 20, 8, 5, QColor(0, 100, 100)),
    ("1.4", 1, 25, 8, 5, QColor(0, 100, 100)),
    ("1.5", 1, 32, 5, 8, QColor(0, 100, 100)),
    ("1.6", 6, 32, 5, 8, QColor(0, 100, 100)),

    ("1.7", 13, 1, 10, 12, QColor(0, 25, 10)),
]

names_list = [item[0] for item in rooms]


def is_valid_name(s):
    res = names_list.count(str(s).lower()) > 0
    Log().send(Log.LogType.INFO, "text = \"" + str(s).lower() + "\", res = " + str(res))
    return res


def get_you_pos():
    return ("", -10, -10, 3)


def get_names_list():
    return names_list


def get_default_floor():
    return 1


def get_floors():
    return [2, 1]


def get_floors_num():
    return 2


def get_walls(floor):
    return walls


def get_empty_rooms(floor):
    return erooms


def get_ladders(floor):
    return ladders


def get_rooms_list(floor):
    return rooms
