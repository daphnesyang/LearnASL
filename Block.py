import math

class Block():
    def __init__(self, x, y, length, width, speed, direction, letter):
        # (x,y) is the coordinate of the leading corner closest to the front
        self.x = x
        self.y = y
        self.length = length
        self.width = width
        self.height = 15 # thickness of block does not change
        self.speed = speed
        self.direction = direction
        self.letter = letter
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
    # def fallingBlock(self, length, width):
    #     
    #         