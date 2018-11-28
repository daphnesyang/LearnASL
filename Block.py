import math

class Block():
    def __init__(self, x, y, length, width, speed, direction, letter):
        # (x,y) is the coordinate of the leading corner closest to the front
        self.x = x
        self.y = y
        self.length = length
        self.width = width
        self.height = 20 # thickness of block does not change
        self.speed = speed
        self.direction = direction
        self.letter = letter
    def getTopPoints(self):
        return [[self.x, self.y],
                [self.x + self.length/math.sqrt(2), self.y - self.length/math.sqrt(2)],
                [self.x + self.length/math.sqrt(2) - self.width/math.sqrt(2), self.y - self.length/math.sqrt(2) - self.width/math.sqrt(2)],
                [self.x - self.width/math.sqrt(2), self.y - self.width/math.sqrt(2)]]
    def getLeftPoints(self):
        return [[self.x, self.y],
                [self.x, self.y + self.height],
                [self.x - self.width/math.sqrt(2), self.y + self.height - self.width/math.sqrt(2)],
                [self.x - self.width/math.sqrt(2), self.y - self.width/math.sqrt(2)]]
    def getRightPoints(self):
        return [[self.x, self.y],
                [self.x, self.y + self.height],
                [self.x + self.length/math.sqrt(2), self.y + self.height - self.length/math.sqrt(2)],
                [self.x + self.length/math.sqrt(2), self.y - self.length/math.sqrt(2)]]
    def getBottomCorner(self):
        return [self.x, self.y]
    def getRightCorner(self):
        return [self.x + self.length/math.sqrt(2), self.y - self.length/math.sqrt(2)]
    def getTopCorner(self):
        return [self.x + self.length/math.sqrt(2) - self.width/math.sqrt(2), self.y - self.length/math.sqrt(2) - self.width/math.sqrt(2)]
    def getLeftCorner(self):
        return [self.x - self.width/math.sqrt(2), self.y - self.width/math.sqrt(2)]
    def getCenter(self):
        return [((self.getBottomCorner()[0] + self.getRightCorner()[0])/2 + (self.getTopCorner()[0] + self.getLeftCorner()[0])/2) / 2,
                ((self.getBottomCorner()[1] + self.getRightCorner()[1])/2 + (self.getTopCorner()[1] + self.getLeftCorner()[1])/2) / 2]
    def moveBlock(self):
        self.y += self.speed
        if self.direction == "right":
            self.x += self.speed
        else:
            self.x -= self.speed
    def chopBlock(self, x, y):
        # (x,y) is the point where it will be cut off
        self.x = x
        self.y = y