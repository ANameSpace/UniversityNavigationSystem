import uuid
from functools import lru_cache


class CorridorlineObj:
    def __init__(self, name: str, x1: int, y1: int, x2: int, y2: int, img_name: str, img_text):
        self.uuid = uuid.uuid4()
        self.name = name

        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.img_name = img_name
        self.img_text = img_text
        self.points = 0


    def getId(self):
        return self.uuid

    def getName(self):
        return self.name

    @lru_cache
    def getLocation(self):
        return tuple([self.x1, self.y1, self.x2, self.y2])

    def getImg(self):
        return self.img_name

    def getText(self):
        return self.img_text
    def getPoints1(self):
        return self.points