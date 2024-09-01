import pyxel


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sprites = {
            'right': ((5, 0), (6, 0)),
            'down': ((7, 0), (8, 0)),
            'up': ((9, 0), (10, 0)),
            'left': ((11, 0), (12, 0)),
        } 
        self.sprite = 0
        self.frames = 0
        self.dir = 'right'

    def checkCol(self):
        print(self.x, self.y)

    def draw(self):
        pyxel.tilemaps[1].pset(self.x, self.y, self.sprites[self.dir][self.sprite])

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

    def reset(self):
        self.dir = 'right'
        self.frames = 0
        self.sprite = 0

    def setDir(self, dir='right'):
        self.dir = dir
        self.sprite = 0
        self.frames = 0

    def update(self):
        self.frames += 1

        if self.frames % 20 == 0:
            self.sprite = 1 if self.sprite == 0 else 0
