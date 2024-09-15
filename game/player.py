import pyxel


class Player:
    """ Class for the player """
    def __init__(self, x: int, y: int):
        """Class constructor

        Args:
            x (int): Starting position of the player from the left
            y (int): Starting position of the player from the top
        """
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

    def draw(self):
        ''' Draw the player sprite on the screen. '''
        pyxel.tilemaps[1].pset(self.x, self.y, self.sprites[self.dir][self.sprite])

    def setPos(self, x: int, y: int):
        """Move the player to the indicated coordinates.

        Args:
            x (int): Setting position of the player from the left
            y (int): Setting position of the player from the top
        """
        self.x = x
        self.y = y

    def move(self, moveDir: str):
        """Move the player in the indicated direction

        Args:
            moveDir (str): The direction in which the player is to be moved
        """
        if moveDir == 'right':
            self.x += 1
        elif moveDir == 'down':
            self.y += 1
        elif moveDir == 'up':
            self.y -= 1
        elif moveDir == 'left':
            self.x -= 1

    def reset(self):
        """ Resets the direction the player faces, the sprites to use and the position of the animation. """
        self.dir = 'right'
        self.frames = 0
        self.sprite = 0

    def setDir(self, dir: str = 'right'):
        """Changes the direction in which the player is facing

        Args:
            dir (str, optional): The direction. Defaults to 'right'.
        """
        self.dir = dir
        self.sprite = 0
        self.frames = 0

    def update(self):
        """ It is called in each frame in order to animate the player. """
        self.frames += 1

        if self.frames % 20 == 0:
            self.sprite = 1 if self.sprite == 0 else 0
