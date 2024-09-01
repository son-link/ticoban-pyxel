import pyxel
from .rock import Rock
from .levels import Levels
from .player import Player
from .constants import SCREEN_H, SCREEN_W, COL_ROCK, COL_WALL
from .pyxel_menu import PyxelMenu


def centerText(text, posy, color):
    '''Centra un texto en pantalla'''
    pyxel.text(
        (SCREEN_W / 2) - ((len(text) * 4) / 2),
        posy, text, color
    )


class Ticoban:
    def __init__(self):
        self.levels = Levels()

        # Main menu
        self.mainMenu = PyxelMenu(72, 96, self.levels.listLevelsFiles)
        self.mainMenu.set_text_color(3)
        self.mainMenu.set_highlight_color(5)
        self.mainMenu.set_cursor_img(0, 104, 0, 0)
        self.levelFile = self.levels.listLevelsFiles[0]
        self.levels.curLevelIndex = 0

        # Pause menu
        self.pauseConf = {
            'start_x': (SCREEN_W / 2) - 28,
            'start_y': ((SCREEN_H / 2) - 14),
        }

        self.pauseMenu = PyxelMenu(
            self.pauseConf['start_x'] + 2,
            self.pauseConf['start_y'] + 12,
            ['Continue', 'Main menu', 'Exit'],
            3
        )
        self.pauseMenu.set_text_color(4)
        self.pauseMenu.set_highlight_color(6)
        self.pauseMenu.set_cursor_img(0, 104, 0, 0)

        self.player = None
        self.rocks = []
        # 1: Main Screen, 2: Selecting level file, 3: Playing
        # 4: Level complete, 5: Pause
        self.game_state = 1
        self.cursorMenuPos = 0
        self.moves = 0

        pyxel.init(SCREEN_W, SCREEN_H, title='Ticoban', display_scale=2,
                   capture_scale=3, capture_sec=40)
        pyxel.load('assets.pyxres')

        pyxel.run(self.update, self.draw)

    def getPlayerRock(self):
        tile_x = self.levels.curLevel['start_x']
        tile_y = self.levels.curLevel['start_y']

        for line in self.levels.curLevel['lines']:
            for char in line:
                if char == '@':
                    self.player = Player(tile_x, tile_y)
                elif char == '$' or char == '*':
                    self.rocks.append(Rock(tile_x, tile_y))

                tile_x += 1

            tile_x = self.levels.curLevel['start_x']
            tile_y += 1

    def update(self):
        btn_pressed = self.getBtnPressed()
        if self.game_state == 1:
            if (
                btn_pressed == 'a' or
                (btn_pressed == 'start' and self.game_state != 3)
            ):
                self.game_state = 2

        elif self.game_state == 2:
            if btn_pressed == 'a' or btn_pressed == 'start':
                self.levels.fileSelected = self.mainMenu.get_current_pos()
                self.levels.loadLevels()
                self.levels.curLevel = self.levels.getLevel(self.levels.curLevelIndex)
                self.getPlayerRock()
                self.game_state = 3

            elif btn_pressed == 'up':
                self.mainMenu.move_up()
            elif btn_pressed == 'down':
                self.mainMenu.move_down()

        elif self.game_state == 3 and self.player:
            self.player.update()
            colide = False
            moveDir = None
            next_x = 0
            next_y = 0

            if btn_pressed == 'left':
                self.player.setDir('left')
                colide, next_x, next_y = self.collide_map(self.player, 'left')
                moveDir = 'left' if colide != COL_WALL else None

            elif btn_pressed == 'right':
                self.player.setDir('right')
                colide, next_x, next_y = self.collide_map(self.player, 'right')
                moveDir = 'right' if colide != COL_WALL else None

            elif btn_pressed == 'up':
                self.player.setDir('up')
                colide, next_x, next_y = self.collide_map(self.player, 'up')
                moveDir = 'up' if colide != COL_WALL else None

            elif btn_pressed == 'down':
                self.player.setDir('down')
                colide, next_x, next_y = self.collide_map(self.player, 'down')
                moveDir = 'down' if colide != COL_WALL else None

            # Reset current level
            if btn_pressed == 'select':
                self.clearMap()
                self.levels.curLevel = self.levels.getLevel(self.levels.current)
                self.getPlayerRock()

            # Show pause menu
            if btn_pressed == 'start':
                self.game_state = 5

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
            if btn_pressed == 'a' or btn_pressed == 'start':
                next_level = self.levels.next()
                if next_level:
                    self.clearMap()
                    self.levels.curLevel = next_level
                    self.getPlayerRock()
                    self.game_state = 3

        # Game paused
        elif self.game_state == 5:
            if btn_pressed == 'a':
                if self.pauseMenu.get_current_pos() == 0:
                    self.game_state = 3
                elif self.pauseMenu.get_current_pos() == 1:
                    self.levelFile = self.levels.listLevelsFiles[0]
                    self.clearMap()
                    self.levels.reset()
                    self.pauseMenu.set_cursor_pos(0)
                    self.game_state = 1
                elif self.pauseMenu.get_current_pos() == 2:
                    pyxel.quit()
            elif btn_pressed == 'up':
                self.pauseMenu.move_up()
            elif btn_pressed == 'down':
                self.pauseMenu.move_down()
            elif btn_pressed == 'start':
                self.pauseMenu.set_cursor_pos(0)
                self.game_state = 3

    def draw(self):
        pyxel.cls(0)

        if self.game_state == 1 or self.game_state == 2:
            pyxel.bltm(0, 0, 0, 0, 0, SCREEN_W, SCREEN_H)
            centerText('Press A (Z key) to start.', 72, 12)
            centerText('(c) 2020 - 2024 Alfonso Saavedra "Son Link"', SCREEN_H - 16, 12)

        if self.game_state == 2:
            centerText('Press UP or DOWN to select file.', 80, 12)
            self.mainMenu.draw()

        elif (
            (self.game_state == 3 and self.levels.curLevel) or
            self.game_state == 4 or
            self.game_state == 5
        ):
            pyxel.bltm(0, 0, 1, 0, 0, SCREEN_W, SCREEN_H)

            # Show movements and map's name
            pyxel.rect(0, 0, SCREEN_W, 8, 15)
            pyxel.text(8, 1, f"Map: {self.levels.curLevel['title']}", 12)
            pyxel.text(SCREEN_W - 48, 1, f'Moves: {self.moves:03}', 12)

            self.levels.draw()

            if self.player:
                self.player.draw()

            if len(self.rocks) > 0:
                for rock in self.rocks:
                    rock.draw()

        if self.game_state == 4:
            pyxel.bltm(0, 0, 1, 0, 0, SCREEN_W, SCREEN_H)
            pyxel.rect(0, 0, SCREEN_W, 8, 15)
            pyxel.text(8, 1, f"Map: {self.levels.curLevel['title']}", 12)
            pyxel.text(SCREEN_W - 48, 1, f'Moves: {self.moves:03}', 12)

            startX = (SCREEN_W / 2) - 40
            startY = (SCREEN_H / 2) - 14
            pyxel.rect(startX, startY, 80, 28, 0)
            centerText('LEVEL COMPLETE', startY + 4, 6)
            centerText('Press A to continue', startY + 16, 12)

        if self.game_state == 5:
            pyxel.rect(self.pauseConf['start_x'], self.pauseConf['start_y'], 52, 36, 0)
            centerText('PAUSE', self.pauseConf['start_y'] + 4, 6)
            self.pauseMenu.draw()

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

        tile_x, tile_y = pyxel.tilemaps[1].pget(x1, y1)
        if tile_x == 2 and tile_y == 0:
            return (COL_WALL, x1, y1)

        if tile_x == 1 and tile_y == 0:
            return (COL_ROCK, x1, y1)

        self.moves += 1
        return (False, x1, y1)

    def compLevelComplete(self):
        in_hole = 0
        for rock in self.rocks:
            x = rock.x - self.levels.curLevel['start_x']
            y = rock.y - self.levels.curLevel['start_y']
            char = self.levels.curLevel['lines'][y][x]
            if char == '.' or char == '*':
                in_hole += 1

        if in_hole == len(self.rocks):
            self.game_state = 4

    def clearMap(self):
        self.levels.genBackground()
        self.levels.curLevel = None
        self.rocks = []
        self.moves = 0
        self.player.reset()

    def getBtnPressed(self):
        if (
            pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP) or
            pyxel.btnp(pyxel.KEY_UP)
        ):
            return 'up'
        elif (
            pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN) or
            pyxel.btnp(pyxel.KEY_DOWN)
        ):
            return 'down'
        elif (
            pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT) or
            pyxel.btnp(pyxel.KEY_LEFT)
        ):
            return 'left'
        elif (
            pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT) or
            pyxel.btnp(pyxel.KEY_RIGHT)
        ):
            return 'right'
        elif (
            pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) or
            pyxel.btnp(pyxel.KEY_Z)
        ):
            return 'a'
        elif (
            pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B) or
            pyxel.btnp(pyxel.KEY_X)
        ):
            return 'b'
        elif (
            pyxel.btnp(pyxel.GAMEPAD1_BUTTON_START) or
            pyxel.btnp(pyxel.KEY_RETURN)
        ):
            return 'start'
        elif (
            pyxel.btnp(pyxel.GAMEPAD1_BUTTON_BACK) or
            pyxel.btnp(pyxel.KEY_SPACE)
        ):
            return 'select'


# tico = Ticoban()
