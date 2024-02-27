import uuid
from functools import lru_cache
import os

from PySide6 import QtGui
from PySide6.QtWidgets import QLabel

from app.utils.tools.Log import Log


class RoomObj:
    def __init__(self, name: str, x: int, y: int, width: int, height: int, img_name: str, flor: str):
        self.uuid = uuid.uuid4()
        self.name = name

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.img_name = img_name

        self.flor = flor

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
        return "Откройте дверь"

    def getflor(self):
        return self.flor

    def getImgL(self):
        img = QtGui.QPixmap(self.img_name)
        if img.isNull():
            Log().send(Log.LogType.ERROR, "Failed to load navigation image!")
        else:
            object = QLabel()
            object.setPixmap(img)
        return object
