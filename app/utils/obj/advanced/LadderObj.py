import uuid
from functools import lru_cache


class LadderObj:
    def __init__(self, name: str, x: int, y: int, width: int, height: int, img_name: str):
        self.uuid = uuid.uuid4()
        self.name = name

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.img_name = img_name

    def getId(self):
        return self.uuid

    def getName(self):
        return self.name

    @lru_cache
    def getLocation(self):
        return tuple([self.x, self.y, self.width, self.height])

    def getImg(self):
        return self.img_name

    def getText(self):
        return "Зайдите на лестницу"
