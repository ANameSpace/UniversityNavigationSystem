import json

from functools import *
import os
import sys

from utils.obj.LadderObj import LadderObj
from utils.obj.RoomObj import RoomObj
from utils.tools.Log import Log

default_data = """
                {
                    "name": "Example",
                    "default": {
                        "id": "MAIN",
                        "floor": "1",
                        "x": "0",
                        "y": "0",
                        "size": "5"
                    },
                    "floors": {
                        "1": {
                            "walls": {
                                "1": {
                                    "x1": "-5",
                                    "y1": "-5",
                                    "x2": "5",
                                    "y2": "5"
                                },
                                "2": {
                                    "x1": "1",
                                    "y1": "3",
                                    "x2": "4",
                                    "y2": "5"
                                }
                            },
                            "empty_rooms": {
                                "1": {
                                    "x": "15",
                                    "y": "15",
                                    "width": "5",
                                    "height": "5"
                                },
                                "2": {
                                    "x": "20",
                                    "y": "15",
                                    "width": "5",
                                    "height": "5"
                                }
                            },
                            "ladders": {
                                "1": {
                                    "x": "20",
                                    "y": "30",
                                    "width": "5",
                                    "height": "5"
                                },
                                "2": {
                                    "x": "20",
                                    "y": "35",
                                    "width": "5",
                                    "height": "5"
                                }
                            },
                            "rooms": {
                                "1.1": {
                                    "x": "10",
                                    "y": "0",
                                    "width": "5",
                                    "height": "4"
                                },
                                "2.1": {
                                    "x": "10",
                                    "y": "5",
                                    "width": "4",
                                    "height": "4"
                                }
                            }
                        },
                        "2": {
                            "walls": {
                                "1": {
                                    "x1": "0",
                                    "y1": "0",
                                    "x2": "10",
                                    "y2": "0"
                                },
                                "2": {
                                    "x1": "0",
                                    "y1": "0",
                                    "x2": "0",
                                    "y2": "10"
                                }
                            },
                            "empty_rooms": {
                                "1": {
                                    "x": "2",
                                    "y": "2",
                                    "width": "5",
                                    "height": "10"
                                },
                                "2": {
                                    "x": "9",
                                    "y": "9",
                                    "width": "5",
                                    "height": "10"
                                }
                            },
                            "ladders": {
                                "1": {
                                    "x": "-10",
                                    "y": "0",
                                    "width": "10",
                                    "height": "10"
                                },
                                "2": {
                                    "x": "-20",
                                    "y": "0",
                                    "width": "10",
                                    "height": "10"
                                }
                            },
                            "rooms": {
                                "3.1": {
                                    "x": "20",
                                    "y": "20",
                                    "width": "10",
                                    "height": "10"
                                },
                                "3.2": {
                                    "x": "20",
                                    "y": "30",
                                    "width": "10",
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
            # Temp
            self.all_names = None
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

    @lru_cache
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

    @lru_cache
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
        """
            Get the number of all floors
            :return: number of all floors
            :rtype: int
        """
        return self.floors_count

    @lru_cache
    def get_default_floor(self):
        """
            Get the default floor name.
            :return: floor name
            :rtype: str
        """
        try:
            return str(self.data["default"]["floor"])
        except:
            Log().send(Log.LogType.ERROR, "The section \"default.floor\" could not be loaded!")
            return 1

    @lru_cache
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
            self.all_names = names
            return tuple(names)
        except:
            Log().send(Log.LogType.ERROR, "The section \"floors.rooms\" could not be loaded!")
            return tuple()

    @lru_cache
    def get_walls(self, floor_name: str):
        """
            Get a list of walls
            :param str floor_name: floor name
            :return: (x1: int, y1: int, x2: int, y2: int)
            :rtype: list
        """
        floor_name = str(floor_name)
        try:
            walls = []
            for f in list(self.data["floors"][floor_name]["walls"].keys()):
                walls.append(tuple([int(self.data["floors"][floor_name]["walls"][f]["x1"]),
                                    int(self.data["floors"][floor_name]["walls"][f]["y1"]),
                                    int(self.data["floors"][floor_name]["walls"][f]["x2"]),
                                    int(self.data["floors"][floor_name]["walls"][f]["y2"])]))
            return walls
        except:
            Log().send(Log.LogType.ERROR, "The section \"floors." + floor_name + ".walls\" could not be loaded!")
            return []

    @lru_cache
    def get_empty_rooms(self, floor_name: str):
        """
            Get a list of empty rooms
            :param str floor_name: floor name
            :return: (x: int, y: int, width: int, height: int)
            :rtype: list
        """
        floor_name = str(floor_name)
        try:
            rooms = []
            for f in list(self.data["floors"][floor_name]["empty_rooms"].keys()):
                rooms.append(tuple([int(self.data["floors"][floor_name]["empty_rooms"][f]["x"]),
                                    int(self.data["floors"][floor_name]["empty_rooms"][f]["y"]),
                                    int(self.data["floors"][floor_name]["empty_rooms"][f]["width"]),
                                    int(self.data["floors"][floor_name]["empty_rooms"][f]["height"])]))
            return rooms
        except:
            Log().send(Log.LogType.ERROR, "The section \"floors." + floor_name + ".empty_rooms\" could not be loaded!")
            return []

    @lru_cache
    def get_ladders(self, floor_name: str):
        """
            Get a list of ladders
            :param str floor_name: floor name
            :return: (LadderObj, LadderObj, ...)
            :rtype: list
        """
        floor_name = str(floor_name)
        try:
            rooms = []
            for f in list(self.data["floors"][floor_name]["empty_rooms"].keys()):
                rooms.append(
                    LadderObj(str(f),
                              int(self.data["floors"][floor_name]["empty_rooms"][f]["x"]),
                              int(self.data["floors"][floor_name]["empty_rooms"][f]["y"]),
                              int(self.data["floors"][floor_name]["empty_rooms"][f]["width"]),
                              int(self.data["floors"][floor_name]["empty_rooms"][f]["height"])))
            return rooms
        except:
            Log().send(Log.LogType.ERROR, "The section \"floors." + floor_name + ".empty_rooms\" could not be loaded!")
            return []

    @lru_cache
    def get_rooms(self, floor_name: str):
        """
            Get a list of rooms
            :param str floor_name: floor name
            :return: (RoomObj, RoomObj, ...)
            :rtype: list
        """
        try:
            rooms = []
            for f in list(self.data["floors"][floor_name]["rooms"].keys()):
                rooms.append(
                    RoomObj(str(f),
                            int(self.data["floors"][floor_name]["rooms"][f]["x"]),
                            int(self.data["floors"][floor_name]["rooms"][f]["y"]),
                            int(self.data["floors"][floor_name]["rooms"][f]["width"]),
                            int(self.data["floors"][floor_name]["rooms"][f]["height"])))
            return rooms
        except:
            Log().send(Log.LogType.ERROR, "The section \"floors." + floor_name + ".rooms\" could not be loaded!")
            return []
