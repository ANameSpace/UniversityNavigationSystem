from functools import lru_cache


class EmptyRoomObj:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @lru_cache
    def getLocation(self):
        return tuple([self.x, self.y, self.width, self.height])
