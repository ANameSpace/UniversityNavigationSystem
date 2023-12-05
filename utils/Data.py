import json

from PySide6.QtGui import QColor
import os

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


class Data:
    _instance = None
    _init_already = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not Data._init_already:
            self.current_directory = os.getcwd()
            self.data_directory = os.path.join(self.current_directory, "UniversityNavigationSystem")
            self.data_file = os.path.join(self.data_directory, "map.json")
            self._generate_file()
            Data._init_already = True

    def _generate_file(self):
        """
           Load map.json file (PROTECTED)
        """
        # Searching for today's latest log file
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                self.data = json.load(file)
        else:
            Log().send(Log.LogType.ERROR, "File map.json was not found! Creating a new file.")
            with open(self.data_file, 'w') as file:
                default_data = """
                {
                	"size": "Medium",
                	"price": 15.67,
                	"toppings": ["Mushrooms", "Extra Cheese", "Pepperoni", "Basil"],
                	"client": {
                		"name": "Jane Doe",
                		"phone": "455-344-234",
                		"email": "janedoe@email.com"
                	}
                }
                """
                self.data = json.loads(default_data)
                json.dump(self.data, file, ensure_ascii=False, indent=4, sort_keys=True)

