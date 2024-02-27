from functools import lru_cache


class WallObj:
    def __init__(self, x1: int, y1: int, x2: int, y2: int):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    @lru_cache
    def getLocation(self):
        return tuple([self.x1, self.y1, self.x2, self.y2])
