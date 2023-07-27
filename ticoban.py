import pyxel
from rock import Rock
from levels import Levels
from player import Player

# Globals
SCREEN_W = 240
SCREEN_H = 136

# Collide values
COL_WALL = 1
COL_ROCK = 2


def centerText(text, posy, color):
    '''Centra un texto en pantalla'''
    pyxel.text(
        (SCREEN_W / 2) - ((len(text) * 4) / 2),
        posy, text, color
    )


class Ticoban:
    def __init__(self):
        self.levels = Levels()
        self.levelFile = self.levels.listLevelsFiles[0]
        self.curLevel = None
        self.curLevelIndex = 0

        self.player = None
        self.rocks = []
        # 1: Main Screen, 2: Selecting level file, 3: Playing
        # 4: Level complete, 5: Game Over
        self.game_state = 1

        # self.level = self.levels.levels[0]
        pyxel.init(SCREEN_W, SCREEN_H, 'Ticoban', display_scale=3,
                   capture_scale=3, capture_sec=20)
        pyxel.load('assets.pyxres')

        pyxel.run(self.update, self.draw)

    def getPlayerRock(self):
        w = self.curLevel['width']
        h = self.curLevel['height']

        self.start_x = pyxel.floor(((30 - w) / 2) - 1)
        self.start_y = pyxel.floor(((17 - h) / 2) - 1)

        tile_x = self.start_x
        tile_y = self.start_y

        for line in self.curLevel['lines']:
            for char in line:
                if char == '@':
                    self.player = Player(tile_x, tile_y)
                elif char == '$' or char == '*':
                    self.rocks.append(Rock(tile_x, tile_y))

                tile_x += 1

            tile_x = self.start_x
            tile_y += 1

    def update(self):
        if self.game_state == 1:
            if (
                pyxel.btnp(pyxel.KEY_Z) or
                (pyxel.btnp(pyxel.KEY_RETURN) and self.game_state != 3) or
                pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A)
            ):
                self.game_state = 2

        elif self.game_state == 2:
            if (
                pyxel.btnp(pyxel.KEY_Z) or
                (pyxel.btnp(pyxel.KEY_RETURN) and self.game_state != 3) or
                pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A)
            ):
                self.levels.loadLevels()
                self.curLevel = self.levels.getLevel(self.curLevelIndex)
                self.getPlayerRock()
                self.game_state = 3

            elif (
                pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP) or
                pyxel.btnp(pyxel.KEY_UP)
            ):
                self.levelFile = self.levels.showLevelsFiles('up')
            elif (
                pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN) or
                pyxel.btnp(pyxel.KEY_DOWN)
            ):
                self.levelFile = self.levels.showLevelsFiles('down')

        elif self.game_state == 3 and self.player:
            colide = False
            moveDir = None
            next_x = 0
            next_y = 0

            if (
                (
                    pyxel.btnp(pyxel.KEY_LEFT) or
                    pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)
                )
            ):
                self.player.setDir('left')
                colide, next_x, next_y = self.collide_map(self.player, 'left')
                moveDir = 'left' if colide != COL_WALL else None

            if (
                (
                    pyxel.btnp(pyxel.KEY_RIGHT) or
                    pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT)
                )
            ):
                self.player.setDir('right')
                colide, next_x, next_y = self.collide_map(self.player, 'right')
                moveDir = 'right' if colide != COL_WALL else None

            if (
                (
                    pyxel.btnp(pyxel.KEY_UP) or
                    pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP)
                )
            ):
                self.player.setDir('up')
                colide, next_x, next_y = self.collide_map(self.player, 'up')
                moveDir = 'up' if colide != COL_WALL else None

            if (
                (
                    pyxel.btnp(pyxel.KEY_DOWN) or
                    pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)
                )
            ):
                self.player.setDir('down')
                colide, next_x, next_y = self.collide_map(self.player, 'down')
                moveDir = 'down' if colide != COL_WALL else None

            if colide == COL_ROCK:
                for rock in self.rocks:
                    if rock.x == next_x and rock.y == next_y:
                        colide1, next_x1, next_y1 = self.collide_map(rock, moveDir)
                        if not colide1:
                            rock.setPos(next_x1, next_y1)
                            self.player.move(moveDir)
                            break

            elif not colide:
                self.player.move(moveDir)

            self.compLevelComplete()

        elif self.game_state == 4:
            if (
                pyxel.btnp(pyxel.KEY_Z) or
                (pyxel.btnp(pyxel.KEY_RETURN) and self.game_state != 3) or
                pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A)
            ):
                next_level = self.levels.next()
                if next_level:
                    self.clearMap()
                    self.curLevel = next_level
                    self.getPlayerRock()
                    self.game_state = 3

    def draw(self):
        tile_x = 0
        tile_y = 0

        pyxel.cls(0)

        if self.game_state == 1 or self.game_state == 2:
            pyxel.bltm(0, 0, 0, 0, 0, SCREEN_W, SCREEN_H)
            centerText('Press A (Z key) to start.', 72, 12)
            centerText('(c) 2020 - 2023 Alfonso Saavedra "Son Link"', 120, 12)

        if self.game_state == 2:
            centerText('Press UP or DOWN to select file.', 80, 12)
            centerText(self.levelFile, 96, 3)

        elif (self.game_state == 3 and self.curLevel) or self.game_state == 4:
            pyxel.bltm(0, 0, 1, 0, 0, SCREEN_W, SCREEN_H)
            w = self.curLevel['width']
            h = self.curLevel['height']

            self.start_x = pyxel.floor(((30 - w) / 2) - 1)
            self.start_y = pyxel.floor(((17 - h) / 2) - 1)

            tile_x = self.start_x
            tile_y = self.start_y

            for line in self.curLevel['lines']:
                draw_floor = False
                for char in line:
                    if char == '#':
                        pyxel.tilemap(1).pset(tile_x, tile_y, (7, 1))
                        draw_floor = True
                    elif char == '.' or char == '*':
                        pyxel.tilemap(1).pset(tile_x, tile_y, (4, 0))
                    else:
                        if char == '':
                            draw_floor = False

                        if draw_floor:
                            pyxel.tilemap(1).pset(tile_x, tile_y, (3, 0))

                    tile_x += 1

                tile_x = self.start_x
                tile_y += 1

            if self.player:
                self.player.draw()

            if len(self.rocks) > 0:
                for rock in self.rocks:
                    rock.draw()

        if self.game_state == 4:
            pyxel.bltm(0, 0, 1, 0, 0, SCREEN_W, SCREEN_H)
            centerText('LEVEL COMPLETE', 64, 6)
            centerText('Press A to continue', 72, 12)

    def loadLevels(self, levelfile):
        self.levels.loadLevels(levelfile)

    def collide_map(self, obj, aim):
        '''Check collisions
            Flags:
                0: the box to move
                1: walls
                2: objetive
                3: player
        '''
        x = obj.x
        y = obj.y
        x1 = 0
        y1 = 0

        if aim == 'left':
            x1 = x - 1
            y1 = y
        elif aim == 'right':
            x1 = x + 1
            y1 = y
        elif aim == 'up':
            x1 = x
            y1 = y - 1
        elif aim == 'down':
            x1 = x
            y1 = y + 1

        tile_x, tile_y = pyxel.tilemap(1).pget(x1, y1)
        if tile_x == 7 and tile_y == 1:
            return (COL_WALL, x1, y1)
        elif tile_x == 1 and tile_y == 0:
            return (COL_ROCK, x1, y1)

        return (False, x1, y1)

    def compLevelComplete(self):
        in_hole = 0
        for rock in self.rocks:
            x = rock.x - self.start_x
            y = rock.y - self.start_y
            char = self.curLevel['lines'][y][x]
            if char == '.' or char == '*':
                in_hole += 1

        if in_hole == len(self.rocks):
            self.game_state = 4

    def clearMap(self):
        w = self.curLevel['width']
        h = self.curLevel['height']

        self.start_x = pyxel.floor(((30 - w) / 2) - 1)
        self.start_y = pyxel.floor(((17 - h) / 2) - 1)

        tile_x = self.start_x
        tile_y = self.start_y

        for line in self.curLevel['lines']:
            for char in line:
                pyxel.tilemap(1).pset(tile_x, tile_y, (0, 0))
                tile_x += 1

            tile_x = self.start_x
            tile_y += 1

        self.curLevel = None
        self.rocks = []


tico = Ticoban()
