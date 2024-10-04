import pyxel
from .rock import Rock
from .levels import Levels
from .player import Player
from . import constants
from .pyxel_menu import PyxelMenu
from .saves import Saves, SAVES_DIR
from os import path


def centerText(text, posy, color):
    '''Centres a text on the screen'''
    pyxel.text(
        (constants.SCREEN_W / 2) - ((len(text) * 4) / 2),
        posy, text, color
    )


class Ticoban:
    def __init__(self):
        self.levels = Levels()

        # Main menu
        self.mainMenu = PyxelMenu(72, 96, limit=3)
        self.mainMenu.set_text_color(3)
        self.mainMenu.set_highlight_color(5)
        self.mainMenu.set_cursor_img(0, 104, 0, 0)
        self.withLoadSave = False

        # Files menu
        self.filesMenu = PyxelMenu(72, 96, self.levels.listLevelsFiles)
        self.filesMenu.set_text_color(3)
        self.filesMenu.set_highlight_color(5)
        self.filesMenu.set_cursor_img(0, 104, 0, 0)
        self.levelFile = self.levels.listLevelsFiles[0]
        self.levels.curLevelIndex = 0

        # Pause menu
        self.pauseConf = {
            'start_x': (constants.SCREEN_W / 2) - 34,
            'start_y': ((constants.SCREEN_H / 2) - 18),
        }

        self.pauseMenu = PyxelMenu(
            self.pauseConf['start_x'] + 2,
            self.pauseConf['start_y'] + 12,
            ['Continue', 'Main menu', 'Save & exit', 'Exit'],
            4
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

        # Init Pyxel and load assets
        pyxel.init(constants.SCREEN_W, constants.SCREEN_H, title='Ticoban', display_scale=3,
                   capture_scale=2, capture_sec=40)
        pyxel.load('assets.pyxres')

        # We check if a save file exists to continue the game.
        if path.isfile(path.join(SAVES_DIR, 'savegame.json')):
            self.withLoadSave = True

        self.setMainMenuOpts()

        self.frame_count = 0
        self.delta_time = 0
        self.previous_time = 0

        # Run the game
        pyxel.run(self.update, self.draw)

    def getPlayerRock(self):
        """Scroll through the level data to get the starting positions of the player and the rocks.
        """
        tile_x = self.levels.curLevel['start_x']
        tile_y = self.levels.curLevel['start_y']

        for line in self.levels.curLevel['lines']:
            for char in line:
                # In the Sokoban format the @ represents the player.
                if char == '@':
                    self.player = Player(tile_x, tile_y)

                # In the case of rocks, the * or $ are the characters that represent them.
                elif char == '$' or char == '*':
                    self.rocks.append(Rock(tile_x, tile_y))

                tile_x += 1

            tile_x = self.levels.curLevel['start_x']
            tile_y += 1

    def update(self):
        """This function is called at each frame, and is where, among other things,
            it checks whether a button or key has been pressed.
        """

        # We get a string that represents that you have pressed
        btn_pressed = self.getBtnPressed()
        if self.game_state == constants.GAME_MAIN_MENU:
            if (btn_pressed == 'a' or btn_pressed == 'start'):
                selected = self.mainMenu.get_current_pos()
                if selected == 0:
                    self.game_state = constants.GAME_SEL_FILE
                elif selected == 1:
                    if self.withLoadSave:
                        self.loadSave()
                    else:
                        pyxel.quit()
                else:
                    pyxel.quit()
            elif btn_pressed == 'up':
                self.mainMenu.move_up()
            elif btn_pressed == 'down':
                self.mainMenu.move_down()

        elif self.game_state == constants.GAME_SEL_FILE:
            if btn_pressed == 'a' or btn_pressed == 'start':
                self.levels.fileSelected = self.filesMenu.get_current_pos()
                self.levels.loadLevels()
                self.levels.curLevel = self.levels.getLevel(self.levels.curLevelIndex)
                self.getPlayerRock()
                self.game_state = constants.GAME_PLAYING
                self.frame_count = 0
                self.levels.genMenuOpts()

            elif btn_pressed == 'up':
                self.filesMenu.move_up()
            elif btn_pressed == 'down':
                self.filesMenu.move_down()

        elif self.game_state == constants.GAME_PLAYING and self.player:
            self.delta_time = self.getTime() - self.previous_time
            self.previous_time = self.getTime()
            self.frame_count += 1
            self.player.update()
            colide = False
            moveDir = None
            next_x = 0
            next_y = 0

            if btn_pressed == 'left':
                self.player.setDir('left')
                colide, next_x, next_y = self.collide_map(self.player, 'left')
                moveDir = 'left' if colide != constants.COL_WALL else None

            elif btn_pressed == 'right':
                self.player.setDir('right')
                colide, next_x, next_y = self.collide_map(self.player, 'right')
                moveDir = 'right' if colide != constants.COL_WALL else None

            elif btn_pressed == 'up':
                self.player.setDir('up')
                colide, next_x, next_y = self.collide_map(self.player, 'up')
                moveDir = 'up' if colide != constants.COL_WALL else None

            elif btn_pressed == 'down':
                self.player.setDir('down')
                colide, next_x, next_y = self.collide_map(self.player, 'down')
                moveDir = 'down' if colide != constants.COL_WALL else None

            # Reset current level
            if btn_pressed == 'select':
                self.clearMap()
                self.levels.curLevel = self.levels.getLevel(self.levels.current)
                self.getPlayerRock()

            # Show pause menu
            if btn_pressed == 'start':
                self.game_state = constants.GAME_PAUSED

            # If the player's collision with a stone was detected, we check whether we can move it in the direction,
            # and if so, we move both
            if colide == constants.COL_ROCK:
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

        elif self.game_state == constants.GAME_LEVEL_COMP:
            if btn_pressed == 'a' or btn_pressed == 'start':
                next_level = self.levels.next()
                if next_level:
                    self.clearMap()
                    self.levels.curLevel = next_level
                    self.getPlayerRock()
                    self.game_state = constants.GAME_PLAYING

        # Game paused
        elif self.game_state == constants.GAME_PAUSED:
            if btn_pressed == 'a':
                if self.pauseMenu.get_current_pos() == 0:
                    self.game_state = constants.GAME_PLAYING
                elif self.pauseMenu.get_current_pos() == 1:
                    self.levelFile = self.levels.listLevelsFiles[0]
                    self.clearMap()
                    self.levels.reset()
                    self.pauseMenu.set_cursor_pos(0)
                    self.setMainMenuOpts()
                    self.game_state = constants.GAME_MAIN_MENU
                elif self.pauseMenu.get_current_pos() == 2:
                    self.saveGame()
                elif self.pauseMenu.get_current_pos() == 3:
                    pyxel.quit()
            elif btn_pressed == 'up':
                self.pauseMenu.move_up()
            elif btn_pressed == 'down':
                self.pauseMenu.move_down()
            elif btn_pressed == 'start':
                self.pauseMenu.set_cursor_pos(0)
                self.game_state = constants.GAME_PLAYING

    def draw(self):
        """This function is called in each frame and inside it is where we
            will indicate what is going to be shown on the screen.
        """

        pyxel.cls(0)

        if self.game_state == constants.GAME_MAIN_MENU or self.game_state == constants.GAME_SEL_FILE:
            pyxel.bltm(0, 0, 0, 0, 0, constants.SCREEN_W, constants.SCREEN_H)
            centerText('Press A (Z key) to start.', 72, 12)
            centerText('(c) 2020 - 2024 Alfonso Saavedra "Son Link"', constants.SCREEN_H - 16, 12)
            if self.game_state == constants.GAME_MAIN_MENU:
                self.mainMenu.draw()

        if self.game_state == constants.GAME_SEL_FILE:
            centerText('Press UP or DOWN to select file.', 80, 12)
            self.filesMenu.draw()

        elif (
            (self.game_state == constants.GAME_PLAYING and self.levels.curLevel) or
            self.game_state == constants.GAME_LEVEL_COMP or
            self.game_state == constants.GAME_PAUSED
        ):
            pyxel.bltm(0, 0, 1, 0, 0, constants.SCREEN_W, constants.SCREEN_H)

            # Show movements, time and map's name
            pyxel.rect(0, 0, constants.SCREEN_W, 8, 15)
            pyxel.text(8, 1, f"Map: {self.levels.curLevel['title']}", 12)
            pyxel.text(constants.SCREEN_W - 48, 1, f'Moves: {self.moves:03}', 12)
            pyxel.text(constants.SCREEN_W - 96, 1, f'Time: {self.getTime():.2f}', 12)

            self.levels.draw()

            if self.player:
                self.player.draw()

            if len(self.rocks) > 0:
                for rock in self.rocks:
                    rock.draw()

        if self.game_state == constants.GAME_LEVEL_COMP:
            pyxel.bltm(0, 0, 1, 0, 0, constants.SCREEN_W, constants.SCREEN_H)
            pyxel.rect(0, 0, constants.SCREEN_W, 8, 15)
            pyxel.text(8, 1, f"Map: {self.levels.curLevel['title']}", 12)
            pyxel.text(constants.SCREEN_W - 48, 1, f'Moves: {self.moves:03}', 12)
            pyxel.text(constants.SCREEN_W - 96, 1, f'Time: {self.getTime():.2f}', 12)

            startX = (constants.SCREEN_W / 2) - 40
            startY = (constants.SCREEN_H / 2) - 14
            pyxel.rect(startX, startY, 80, 28, 0)
            centerText('LEVEL COMPLETE', startY + 4, 6)
            centerText('Press A to continue', startY + 16, 12)

        if self.game_state == constants.GAME_PAUSED:
            pyxel.rect(self.pauseConf['start_x'], self.pauseConf['start_y'], 64, 44, 0)
            centerText('PAUSE', self.pauseConf['start_y'] + 4, 6)
            self.pauseMenu.draw()

    def loadLevels(self, levelfile: str):
        """Sets the file with the levels to be used

        Args:
            levelfile (str): The filename of the levels file
        """
        self.levels.levelsFile = levelfile

    def loadSave(self):
        """ Loads the save file and calls the methods and sets the necessary variables. """
        save = Saves.open('savegame')
        self.levels.loadLevelsFile(save['level_file'])
        self.levels.curLevel = self.levels.getLevel(save['level'])
        self.levelFile = self.levels.listLevelsFiles[save['level']]
        self.levels.curLevelIndex = save['level']
        self.player = Player(save['player']['x'], save['player']['y'])
        self.player.dir = save['player']['direction']
        self.moves = save['moves']
        self.frame_count = save['frame_count']

        for rock in save['rocks']:
            self.rocks.append(Rock(rock['x'], rock['y']))

        self.game_state = constants.GAME_PLAYING
        Saves.delete('savegame')
        self.withLoadSave = False

    def collide_map(self, obj: object, aim: str):
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
            return (constants.COL_WALL, x1, y1)

        if tile_x == 1 and tile_y == 0:
            return (constants.COL_ROCK, x1, y1)

        self.moves += 1
        return (False, x1, y1)

    def compLevelComplete(self):
        """ After each movement this method is called to check if the level was completed. """
        in_hole = 0  # Here we will store how many rocks are found at the target points.
        for rock in self.rocks:
            x = rock.x - self.levels.curLevel['start_x']
            y = rock.y - self.levels.curLevel['start_y']
            char = self.levels.curLevel['lines'][y][x]
            if char == '.' or char == '*':
                in_hole += 1

        # If the value of in_hole is the same as the number of rocks, the level is complete.
        if in_hole == len(self.rocks):
            self.game_state = constants.GAME_LEVEL_COMP
            self.levels.saveScore(self.moves, float(f'{self.getTime():.2f}'))

    def clearMap(self):
        """ Clean the map """
        self.levels.genBackground()
        self.levels.curLevel = None
        self.rocks = []
        self.moves = 0
        self.player.reset()
        self.frame_count = 0

    def getBtnPressed(self):
        """Detects which button or key is pressed and returns a text string representing what was pressed

        Returns:
            str: A text string representing what was pressed
        """
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

    def getTime(self):
        return (self.frame_count * 1) / 60

    def saveGame(self):
        """ Save the current state of the game so that you can continue it at a later time. """
        rocks = []
        for rock in self.rocks:
            rocks.append({
                'x': rock.x,
                'y': rock.y
            })

        data = {
            'player': {
                'x': self.player.x,
                'y': self.player.y,
                'direction': self.player.dir
            },
            'rocks': rocks,
            'moves': self.moves,
            'level_file': self.levels.get_cur_levels_file(),
            'level': self.levels.current,
            'frame_count': self.frame_count
        }

        Saves.save(data, 'savegame')
        pyxel.quit()

    def setMainMenuOpts(self):
        """ Defines the main menu options depending on whether or not the save file exists. """
        if path.isfile(path.join(SAVES_DIR, 'savegame.json')):
            self.mainMenu.set_options(['Start', 'Load save', 'Exit'])
        else:
            self.mainMenu.set_options(['Start', 'Exit'])
