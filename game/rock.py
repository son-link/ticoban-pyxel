import pyxel


class Rock:
    ''' Class for game rocks '''
    def __init__(self, x: int, y: int):
        """Class constructor

        Args:
            x (int): Starting position of the rock from the left
            y (int): Starting position of the rock from the top
        """
        self.x = x
        self.y = y
        self.sprite = (1, 0)

    def draw(self):
        ''' Draw the rock sprite on the screen. '''
        pyxel.tilemaps[1].pset(self.x, self.y, self.sprite)

    def setPos(self, x: int, y: int):
        """Move the rock to the indicated coordinates.

        Args:
            x (int): Setting position of the rock from the left
            y (int): Setting position of the rock from the top
        """
        self.x = x
        self.y = y

    def move(self, moveDir: str):
        """Move the rock in the indicated direction

        Args:
            moveDir (str): The direction in which the rock is to be moved
        """
        if moveDir == 'right':
            self.x += 1
        elif moveDir == 'down':
            self.y += 1
        elif moveDir == 'up':
            self.y -= 1
        elif moveDir == 'left':
            self.x -= 1
