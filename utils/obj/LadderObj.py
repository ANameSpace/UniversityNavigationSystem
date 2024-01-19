class LadderObj:
    def __init__(self, name: str, x: int, y: int, width: int, height: int):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def getLocation(self):
        return tuple([self.x, self.y, self.width, self.height])

    def getName(self):
        return self.name

    def getCorridor(self):
        return "self.name"