import json

from functools import *
import os
import sys

from app.utils.obj.advanced.CorridorlineObj import CorridorlineObj
from app.utils.obj.simple.EmptyRoomObj import EmptyRoomObj
from app.utils.obj.advanced.LadderObj import LadderObj
from app.utils.obj.advanced.RoomObj import RoomObj
from app.utils.obj.simple.WallObj import WallObj
from app.utils.tools.Log import Log

default_data = """
                {
                    "name": "MIREA",
                    "default": {
                        "id": "MAIN",
                        "floor": "1",
                        "x": "22",
                        "y": "40",
                        "size": "2"
                    },
                    "floors": {
                        "1": {
                            "walls": {
                                "1": {
                                    "x1": "0",
                                    "y1": "0",
                                    "x2": "45",
                                    "y2": "0"
                                },
                                "2": {
                                    "x1": "45",
                                    "y1": "0",
                                    "x2": "45",
                                    "y2": "45"
                                },
                                "3": {
                                    "x1": "45",
                                    "y1": "45",
                                    "x2": "0",
                                    "y2": "45"
                                },
                                "4": {
                                    "x1": "0",
                                    "y1": "45",
                                    "x2": "0",
                                    "y2": "0"
                                }
                            },
                            "empty_rooms": {
                                "103": {
                                    "x": "0",
                                    "y": "35",
                                    "width": "7",
                                    "height": "10"
                                },
                                "105-2": {
                                    "x": "0",
                                    "y": "13",
                                    "width": "10",
                                    "height": "5"
                                },
                                "106-2": {
                                    "x": "0",
                                    "y": "0",
                                    "width": "8",
                                    "height": "10"
                                },
                                "106-3": {
                                    "x": "18",
                                    "y": "0",
                                    "width": "16",
                                    "height": "10"
                                },
                                "o": {
                                    "x": "35",
                                    "y": "38",
                                    "width": "10",
                                    "height": "7"
                                }
                            },
                            "ladders": {
                                "1": {
                                    "x": "16",
                                    "y": "30",
                                    "width": "5",
                                    "height": "7"
                                },
                                "2": {
                                    "x": "28",
                                    "y": "30",
                                    "width": "5",
                                    "height": "7"
                                }
                            },
                            "rooms": {
                                "101": {
                                    "x": "14",
                                    "y": "10",
                                    "width": "20",
                                    "height": "20"
                                },
                                "102": {
                                    "x": "7",
                                    "y": "35",
                                    "width": "7",
                                    "height": "10"
                                },
                                "104": {
                                    "x": "0",
                                    "y": "23",
                                    "width": "10",
                                    "height": "7"
                                },
                                "105": {
                                    "x": "0",
                                    "y": "18",
                                    "width": "10",
                                    "height": "5"
                                },
                                "106": {
                                    "x": "8",
                                    "y": "0",
                                    "width": "10",
                                    "height": "10"
                                },
                                "108": {
                                    "x": "38",
                                    "y": "19",
                                    "width": "7",
                                    "height": "15"
                                },
                                "109": {
                                    "x": "38",
                                    "y": "6",
                                    "width": "7",
                                    "height": "10"
                                },
                                "110": {
                                    "x": "34",
                                    "y": "0",
                                    "width": "11",
                                    "height": "6"
                                }
                            },
                            "corridor": {
                                "1.1-1.23": {
                                    "x1": "10",
                                    "y1": "3",
                                    "x2": "10",
                                    "y2": "5",
                                    "a" : ["1.1", "somestring2"]
                                },
                                "1.1-1.23": {
                                    "x1": "10",
                                    "y1": "3",
                                    "x2": "10",
                                    "y2": "5",
                                    "a" : ["1.1", "somestring2"]
                                }
                            }
                        },
                        "2": {
                            "walls": {
                                "1": {
                                    "x1": "0",
                                    "y1": "0",
                                    "x2": "45",
                                    "y2": "0"
                                },
                                "2": {
                                    "x1": "45",
                                    "y1": "0",
                                    "x2": "45",
                                    "y2": "45"
                                },
                                "3": {
                                    "x1": "45",
                                    "y1": "45",
                                    "x2": "0",
                                    "y2": "45"
                                },
                                "4": {
                                    "x1": "0",
                                    "y1": "45",
                                    "x2": "0",
                                    "y2": "0"
                                }
                            },
                            "ladders": {
                                "1": {
                                    "x": "16",
                                    "y": "30",
                                    "width": "5",
                                    "height": "7"
                                },
                                "2": {
                                    "x": "28",
                                    "y": "30",
                                    "width": "5",
                                    "height": "7"
                                }
                            },
                            "empty_rooms": {
                                "200-2": {
                                    "x": "14",
                                    "y": "10",
                                    "width": "19",
                                    "height": "2"
                                },
                                "204-2": {
                                    "x": "38",
                                    "y": "10",
                                    "width": "7",
                                    "height": "8"
                                },
                                "204-3": {
                                    "x": "0",
                                    "y": "10",
                                    "width": "14",
                                    "height": "16"
                                }
                            },
                            "rooms": {
                                "200": {
                                    "x": "14",
                                    "y": "12",
                                    "width": "20",
                                    "height": "18"
                                },
                                "201": {
                                    "x": "0",
                                    "y": "0",
                                    "width": "10",
                                    "height": "7"
                                },
                                "202": {
                                    "x": "10",
                                    "y": "0",
                                    "width": "15",
                                    "height": "7"
                                },
                                "203": {
                                    "x": "25",
                                    "y": "0",
                                    "width": "15",
                                    "height": "7"
                                },
                                "204": {
                                    "x": "40",
                                    "y": "0",
                                    "width": "5",
                                    "height": "10"
                                },
                                "206": {
                                    "x": "38",
                                    "y": "18",
                                    "width": "7",
                                    "height": "12"
                                },
                                "208": {
                                    "x": "0",
                                    "y": "26",
                                    "width": "14",
                                    "height": "10"
                                },
                                "207": {
                                    "x": "0",
                                    "y": "36",
                                    "width": "14",
                                    "height": "9"
                                }
                            },
                            "corridor": {
                                "208-207-f2": {
                                    "x1": "10",
                                    "y1": "3",
                                    "x2": "10",
                                    "y2": "5",
                                    "a1": ["208", "207"],
                                    "a2": "5"
                                },
                                "1.1-1.3": {
                                    "x1": "10",
                                    "y1": "3",
                                    "x2": "10",
                                    "y2": "5",
                                    "a" : ["1.1", "somestring2"]
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
            self.img_directory = os.path.join(self.data_directory, "images")
            if not os.path.exists(self.img_directory):
                os.makedirs(self.img_directory)
            self.data_file = os.path.join(self.data_directory, "map.json")
            self._generate_file()
            # Temp
            self.all_names = None
            self.all_rooms = {}
            Data._init_already = True
            self.all_lines = {}

            self.get_lines("1")
            self.get_lines("2")

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
            self.data = json.loads(default_data)
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

    def get_rooms_by_name(self, name: str):
        """
            Get room by name
            :param str name: room name
            :return: room object
            :rtype: RoomObj
        """
        if self.is_valid_name(name):
            return self.all_rooms.get(name)
        else:
            Log().send(Log.LogType.ERROR, "The room \"" + str(name) + "\" does not exist!")
            return None

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
                self.get_rooms(f)
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
            :return: (WallObj, WallObj, ...)
            :rtype: list
        """
        floor_name = str(floor_name)
        try:
            walls = []
            for f in list(self.data["floors"][floor_name]["walls"].keys()):
                walls.append(WallObj(
                    int(self.data["floors"][floor_name]["walls"][f]["x1"]),
                    int(self.data["floors"][floor_name]["walls"][f]["y1"]),
                    int(self.data["floors"][floor_name]["walls"][f]["x2"]),
                    int(self.data["floors"][floor_name]["walls"][f]["y2"])
                ))
            return walls
        except:
            Log().send(Log.LogType.ERROR, "The section \"floors." + floor_name + ".walls\" could not be loaded!")
            return []

    @lru_cache
    def get_empty_rooms(self, floor_name: str):
        """
            Get a list of empty rooms
            :param str floor_name: floor name
            :return: (EmptyRoomObj, EmptyRoomObj, ...)
            :rtype: list
        """
        floor_name = str(floor_name)
        try:
            rooms = []
            for f in list(self.data["floors"][floor_name]["empty_rooms"].keys()):
                rooms.append(EmptyRoomObj(
                    int(self.data["floors"][floor_name]["empty_rooms"][f]["x"]),
                    int(self.data["floors"][floor_name]["empty_rooms"][f]["y"]),
                    int(self.data["floors"][floor_name]["empty_rooms"][f]["width"]),
                    int(self.data["floors"][floor_name]["empty_rooms"][f]["height"])
                ))
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
            for f in list(self.data["floors"][floor_name]["ladders"].keys()):
                rooms.append(
                    LadderObj(str(f),
                              int(self.data["floors"][floor_name]["ladders"][f]["x"]),
                              int(self.data["floors"][floor_name]["ladders"][f]["y"]),
                              int(self.data["floors"][floor_name]["ladders"][f]["width"]),
                              int(self.data["floors"][floor_name]["ladders"][f]["height"]), ""))
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
                tro = RoomObj(str(f),
                            int(self.data["floors"][floor_name]["rooms"][f]["x"]),
                            int(self.data["floors"][floor_name]["rooms"][f]["y"]),
                            int(self.data["floors"][floor_name]["rooms"][f]["width"]),
                            int(self.data["floors"][floor_name]["rooms"][f]["height"]), os.path.join(self.img_directory, floor_name + "." + f + ".png"), floor_name)
                rooms.append(tro)
                self.all_rooms[tro.getName()] = tro
            return rooms
        except:
            Log().send(Log.LogType.ERROR, "The section \"floors." + floor_name + ".rooms\" could not be loaded!")
            return []

    @lru_cache
    def get_lines(self, floor_name: str):
        """
            Get a list of lines
            :param str floor_name: floor name
            :return: (Obj, Obj, ...)
            :rtype: list
        """
        # try:
        lines = []
        if floor_name == "2":
                tro2 = CorridorlineObj(str("208-207-f2"),
                                  int(19),
                                  int(38),
                                  int(14),
                                  int(38),
                                  os.path.join(self.img_directory, "corridor.f2-t-108.png"),
                                  str("Поверните направо и пройдите перёд"))
                self.all_lines[str(tro2.getName())] = tro2
                lines.append(tro2)

                tro2 = CorridorlineObj(str("200-f2"),
                                       int(19),
                                       int(38),
                                       int(25),
                                       int(38),
                                       os.path.join(self.img_directory, "corridor.200-f2.png"),
                                       str("Поверните налево и пройдите перёд"))
                self.all_lines[str(tro2.getName())] = tro2
                lines.append(tro2)

                tro2 = CorridorlineObj(str("f2-t"),
                                       int(25),
                                       int(38),
                                       int(36),
                                       int(38),
                                       os.path.join(self.img_directory, "corridor.f2-t.png"),
                                       str("Пройдите перёд и поверните налево"))
                self.all_lines[str(tro2.getName())] = tro2
                lines.append(tro2)

                tro2 = CorridorlineObj(str("f2-t-206"),
                                       int(36),
                                       int(38),
                                       int(36),
                                       int(27),
                                       os.path.join(self.img_directory, "corridor.f2-t-206.png"),
                                       str("Пройдите перёд"))
                self.all_lines[str(tro2.getName())] = tro2
                lines.append(tro2)

                tro2 = CorridorlineObj(str("f2-t-203-204"),
                                       int(36),
                                       int(27),
                                       int(36),
                                       int(8),
                                       os.path.join(self.img_directory, "corridor.f2-t-203-204.png"),
                                       str("Пройдите перёд"))
                self.all_lines[str(tro2.getName())] = tro2
                lines.append(tro2)

                tro2 = CorridorlineObj(str("f2-t-201-202"),
                                       int(36),
                                       int(8),
                                       int(10),
                                       int(8),
                                       os.path.join(self.img_directory, "corridor.f2-t-201-202.png"),
                                       str("Пройдите перёд"))
                self.all_lines[str(tro2.getName())] = tro2
                lines.append(tro2)
            # for f in list(self.data["floors"][floor_name]["corridor"].keys()):
            #     tro2 = CorridorlineObj(str(f),
            #                   int(self.data["floors"][floor_name]["corridor"][f]["x1"]),
            #                   int(self.data["floors"][floor_name]["corridor"][f]["y1"]),
            #                   int(self.data["floors"][floor_name]["corridor"][f]["x2"]),
            #                   int(self.data["floors"][floor_name]["corridor"][f]["y2"]),
            #                   os.path.join(self.img_directory, "corridor" + floor_name + "." + f + ".png"),
            #                   int(self.data["floors"][floor_name]["corridor"][f]["text"]),
            #                   list(self.data["floors"][floor_name]["corridor"][f]["a"]))
            #     lines.append(tro2)
            #     self.all_lines[tro2.getName()] = tro2
        else:
            tro2 = CorridorlineObj(str("f1-t-108"),
                                   int(22),
                                   int(38),
                                   int(37),
                                   int(37),
                                   os.path.join(self.img_directory, "corridor.f1-t-108.png"),
                                   str("Поверните направо и пройдите перёд"))
            self.all_lines[str(tro2.getName())] = tro2
            lines.append(tro2)

            tro2 = CorridorlineObj(str("f1-t-110-109"),
                                   int(37),
                                   int(37),
                                   int(37),
                                   int(15),
                                   os.path.join(self.img_directory, "corridor.f1-t-110-109.png"),
                                   str("Пройдите перёд"))
            self.all_lines[str(tro2.getName())] = tro2
            lines.append(tro2)

        return lines
        # except:
        #     Log().send(Log.LogType.ERROR, "The section \"floors." + floor_name + ".corridor\" could not be loaded!")
        #     return []

    def get_patch_to_image(self, name: str):
        return os.path.join(self.img_directory, name)

    @lru_cache
    def get_lines_by_name(self, name: str):
        return self.all_lines.get(name)