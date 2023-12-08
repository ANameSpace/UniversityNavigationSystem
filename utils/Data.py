import json

from PySide6.QtGui import QColor
import os
import sys

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

default_data = """
                {
                    "name": "Example",
                    "default": {
                        "id": "1",
                        "floor": "1",
                        "x": "0",
                        "y": "0",
                        "size": "10"
                    },
                    "floors": {
                        "1": {
                            "walls": {
                                "1": {
                                    "x1": "1",
                                    "y1": "0",
                                    "x2": "0",
                                    "y2": "10"
                                },
                                "2": {
                                    "x1": "1",
                                    "y1": "0",
                                    "x2": "0",
                                    "y2": "10"
                                },
                                "3": {
                                    "x1": "1",
                                    "y1": "0",
                                    "x2": "0",
                                    "y2": "10"
                                }
                            },
                            "empty_rooms": {
                                "1": {
                                    "x1": "1",
                                    "y1": "0",
                                    "width": "0",
                                    "height": "10"
                                },
                                "2": {
                                    "x1": "1",
                                    "y1": "0",
                                    "width": "0",
                                    "height": "10"
                                }
                            },
                            "ladders": {
                                "1": {
                                    "x1": "1",
                                    "y1": "0",
                                    "width": "0",
                                    "height": "10"
                                },
                                "2": {
                                    "x1": "1",
                                    "y1": "0",
                                    "width": "0",
                                    "height": "10"
                                }
                            },
                            "rooms": {
                                "1.1": {
                                    "x1": "1",
                                    "y1": "0",
                                    "width": "0",
                                    "height": "10"
                                },
                                "2.1": {
                                    "x1": "1",
                                    "y1": "0",
                                    "width": "0",
                                    "height": "10"
                                }
                            }
                        },
                        "2": {
                            "walls": {
                                "1": {
                                    "x1": "1",
                                    "y1": "0",
                                    "x2": "0",
                                    "y2": "10"
                                },
                                "2": {
                                    "x1": "1",
                                    "y1": "0",
                                    "x2": "0",
                                    "y2": "10"
                                },
                                "3": {
                                    "x1": "1",
                                    "y1": "0",
                                    "x2": "0",
                                    "y2": "10"
                                }
                            },
                            "empty_rooms": {
                                "1": {
                                    "x1": "1",
                                    "y1": "0",
                                    "width": "0",
                                    "height": "10"
                                },
                                "2": {
                                    "x1": "1",
                                    "y1": "0",
                                    "width": "0",
                                    "height": "10"
                                }
                            },
                            "ladders": {
                                "1": {
                                    "x1": "1",
                                    "y1": "0",
                                    "width": "0",
                                    "height": "10"
                                },
                                "2": {
                                    "x1": "1",
                                    "y1": "0",
                                    "width": "0",
                                    "height": "10"
                                }
                            },
                            "rooms": {
                                "3.1": {
                                    "x1": "1",
                                    "y1": "0",
                                    "width": "0",
                                    "height": "10"
                                },
                                "3.2": {
                                    "x1": "1",
                                    "y1": "0",
                                    "width": "0",
                                    "height": "10"
                                }
                            }
                        }
                    }
                }
                """


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
        # Creating or uploading a file
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                try:
                    self.data = json.load(file)
                except json.decoder.JSONDecodeError:
                    Log().send(Log.LogType.WARNING, "File map.json is corrupted or contains a JSON validation error.")
                    sys.exit()
        else:
            Log().send(Log.LogType.WARNING, "File map.json was not found! Creating a new file.")
            with open(self.data_file, 'w') as file:
                self.data = json.loads(default_data)
                json.dump(self.data, file, ensure_ascii=False, indent=4, sort_keys=True)
        # Some constant data that is frequently accessed. Created for optimization and acceleration.
        try:
            self.you_pos = (
                str(self.data["default"]["id"]), int(self.data["default"]["size"]), int(self.data["default"]["x"]), int(self.data["default"]["y"]))
            self.floors_count = len(list(self.data["floors"].keys()))
        except:
            Log().send(Log.LogType.ERROR, "The section \"default\" could not be loaded!")
            self.you_pos = ("you_pos", 10, 0, 0)
            self.floors_count = 1

    def is_valid_name(self, name: str):
        """
            Checking the existence of a room by its name
            :param str name: room name
            :return: result
            :rtype: bool
        """
        result = name in self.all_names
        Log().send(Log.LogType.INFO, "Find use: text = \"" + str(name).lower() + "\", result = " + str(result))
        return result

    def get_name(self):
        """
            Get the name of the plan
            :return: name
            :rtype: str
        """
        try:
            return str(self.data["name"])
        except:
            Log().send(Log.LogType.ERROR, "The section \"name\" could not be loaded!")
            return "NAME"

    def get_you_pos(self):
        """
            Get the information stand position
            :return: (id: str, size: int, x: int, y: int)
            :rtype: tuple
        """
        return self.you_pos

    def get_floors(self):
        """
            Get a list of names of all floors
            :return: (name1: str, name2: str ...)
            :rtype: tuple
        """
        try:
            return tuple(sorted(self.data["floors"].keys(), reverse=True))
        except:
            Log().send(Log.LogType.ERROR, "The section \"floors\" could not be loaded!")
            return tuple("1")

    def get_floors_count(self):
        return self.floors_count

    def get_default_floor(self):
        """
            Get the default floor name.
            :return: floor name
            :rtype: str
        """
        try:
            return str(self.data["default"]["floor"])
        except:
            Log().send(Log.LogType.ERROR, "The section \"default.floors\" could not be loaded!")
            return 1

    def get_rooms_names(self):
        """
            Get a list of names of all rooms
            :return: (name1: str, name2: str ...)
            :rtype: tuple
        """
        try:
            names = []
            for f in list(self.data["floors"].keys()):
                names += [n for n in self.data["floors"][f]["rooms"]]
            self.all_names = tuple(names)
            return tuple(names)
        except:
            Log().send(Log.LogType.ERROR, "The section \"floors.rooms\" could not be loaded!")
            return tuple()

    def get_walls(self, floor: str):
        return walls

    def get_empty_rooms(self, floor: str):
        return erooms

    def get_ladders(self, floor: str):
        return ladders

    def get_rooms(self, floor: str):
        return rooms
