import pyxel


class Rock:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sprite = (1, 0)

    def checkCol(self):
        print(self.x, self.y)

    def draw(self):
        pyxel.tilemaps[1].pset(self.x, self.y, self.sprite)

    def setPos(self, x, y):
        self.x = x
        self.y = y

    def move(self, moveDir):
        if moveDir == 'right':
            self.x += 1
        elif moveDir == 'down':
            self.y += 1
        elif moveDir == 'up':
            self.y -= 1
        elif moveDir == 'left':
            self.x -= 1
