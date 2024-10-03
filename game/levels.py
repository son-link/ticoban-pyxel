from os import listdir, path
import sys
import pyxel
from .saves import Saves, SAVES_DIR
from pathlib import Path

__dir = ''
if getattr(sys, 'frozen', False):
    __dir = path.dirname(sys.executable)
elif __file__:
    __dir = path.dirname(__file__)

LEVELS_DIR = path.join(__dir, 'levels')


class Levels:
    def __init__(self):
        self.listLevelsFiles = []
        self.fileSelected = 0
        self.levels = []
        self.levelsFile = None
        self.total = 0
        self.current = 0
        self.curLevel = None
        self.levelsScore = []
        self.saveName = ''

        for f in sorted(listdir(LEVELS_DIR)):
            self.listLevelsFiles.append(f)

    def draw(self):
        ''' Draw the level '''
        tile_x = self.curLevel['start_x']
        tile_y = self.curLevel['start_y']

        for line in self.curLevel['lines']:
            draw_floor = False
            for char in line:
                if char == '#':
                    pyxel.tilemaps[1].pset(tile_x, tile_y, (2, 0))
                    draw_floor = True
                elif char == '.' or char == '*':
                    pyxel.tilemaps[1].pset(tile_x, tile_y, (4, 0))
                else:
                    if char == '':
                        draw_floor = False

                    if draw_floor:
                        pyxel.tilemaps[1].pset(tile_x, tile_y, (3, 0))

                tile_x += 1

            tile_x = self.curLevel['start_x']
            tile_y += 1

    def loadLevels(self):
        """ Loads the levels of the file indicated in the position selected in the selection menu. """
        self.levelsFile = self.listLevelsFiles[self.fileSelected]
        self.total = 0
        self.current = 0

        with open(path.join(LEVELS_DIR, self.levelsFile), 'r', encoding='utf-8') as data:
            levelStartLine = 0
            levelEnd = True
            width = 0
            lastLine = ''
            totalLines = 0

            for i, line in enumerate(data):
                line = line.replace('\n', '').lower()
                lastLine = line
                totalLines += 1

                if len(line) > 0:
                    if line.startswith('title'):
                        if not levelEnd:
                            self.levels.append({
                                'start': levelStartLine,
                                'end': i,
                                'width': width,
                                'title': line.replace('title:', '').strip()
                            })
                            levelEnd = True
                            width = 0
                    elif (
                        (line.startswith('#') or line.startswith(' ')) and
                        levelEnd
                    ):
                        levelStartLine = i
                        levelEnd = False
                    elif not levelEnd and not (line.startswith('#') or line.startswith(' ')):
                        if not levelEnd:
                            self.levels.append({
                                'start': levelStartLine,
                                'end': i,
                                'width': width,
                                'title': line.replace('title:', '').strip()
                            })
                            levelEnd = True
                            width = 0

                    if not levelEnd and len(line) > width:
                        width = len(line)

            if not levelEnd:
                end = totalLines if '#' in lastLine else totalLines - 1
                self.levels.append({
                    'start': levelStartLine,
                    'end': end,
                    'width': width,
                    'title': f'Level {len(self.levels) + 1}'
                })

            data.close()
            self.total = len(self.levels)
            self.levelsScore = []

            # Load saves or create new one
            self.saveName = Path(self.levelsFile).stem
            savefile = path.join(SAVES_DIR, f'{self.saveName}.json')
            if not path.isfile(savefile):
                for i in range(0, self.total):
                    self.levelsScore.append({
                        'steps': 0,
                        'time': 0.00
                    })

                Saves.save(self.levelsScore, self.saveName)
            else:
                self.levelsScore = Saves.open(self.saveName)

    def loadLevelsFile(self, filename: str):
        """ Loads the levels of the file indicated.

        Args:
            filename (str): The name of the file with the levels

        Returns:
            bool: If the file was found in the list of found files
        """
        for i in range(len(self.listLevelsFiles)):
            if self.listLevelsFiles[i] == filename:
                self.fileSelected = i
                self.loadLevels()
                return True

        return False

    def getLevel(self, index: int):
        """Loads the level at the indicated position in the level list and returns a dictionary with its data.

        Args:
            index (int): The position of the level in the list of levels

        Returns:
            dict: A dictionary with the level data
        """
        data = self.levels[index]
        lines = []

        with open(path.join(LEVELS_DIR, self.levelsFile), 'r', encoding='utf8') as f:
            for fline in f.readlines()[data['start']:data['end']]:
                line = []
                for i in range(data['width']):
                    line.append('')

                for i, char in enumerate(fline.replace('\n', '')):
                    line[i] = char

                lines.append(line)
            f.close()

        width = data['width']
        height = data['end'] - data['start']

        start_x = pyxel.floor(((30 - width) / 2) + 1)
        start_y = pyxel.floor(((22 - height) / 2))
        self.genBackground()

        level = {
            'width': width,
            'height': height,
            'lines': lines,
            'start_x': start_x,
            'start_y': start_y,
            'title': data['title']
        }

        self.curLevel = level
        return level

    def next(self):
        """Load the next level, if available

        Returns:
            bool: If it was possible to move to the next level
        """
        if self.current < self.total:
            self.current += 1
            return self.getLevel(self.current)

        return False

    def reset(self):
        """ Reset the level """
        self.fileSelected = 0
        self.levels = []
        self.levelsFile = None
        self.total = 0
        self.current = 0

    def genBackground(self):
        """ Randomly generates the outer background of the level. """
        for y in range(22):
            for x in range(30):
                rand = pyxel.rndi(1, 20)
                if rand < 6:
                    pyxel.tilemaps[1].pset(x, y, (14, 0))
                elif rand >= 6 and rand < 10:
                    pyxel.tilemaps[1].pset(x, y, (15, 0))
                elif rand >= 10 and rand < 14:
                    pyxel.tilemaps[1].pset(x, y, (16, 0))
                elif rand >= 14 and rand < 17:
                    pyxel.tilemaps[1].pset(x, y, (17, 0))
                else:
                    pyxel.tilemaps[1].pset(x, y, (18, 0))

    def get_cur_levels_file(self):
        """ Returns the name of the current level file """
        return self.listLevelsFiles[self.fileSelected]

    def saveScore(self, steps: int, time: float):
        """Saves the current level score, provided that the current score is 0 (not yet played), or the score received is lower.

        Args:
            steps (int): The number of moves made by the player
        """
        current_score = self.levelsScore[self.current]['steps']
        current_time = float(self.levelsScore[self.current]['time'])
        save = False

        if current_score == 0 or steps < current_score:
            self.levelsScore[self.current]['steps'] = steps
            save = True

        if current_time == 0.00 or time < current_time:
            self.levelsScore[self.current]['time'] = time
            save = True

        if save:
            Saves.save(self.levelsScore, self.saveName)
