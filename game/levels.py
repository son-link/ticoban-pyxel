from os import listdir, path
import sys
import pyxel

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
                    pyxel.tilemaps[1].pset(tile_x, tile_y, (7, 1))
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

                    if not levelEnd and len(line) > width:
                        width = len(line)

            if not levelEnd:
                end = totalLines if '#' in lastLine else totalLines - 1
                self.levels.append({
                    'start': levelStartLine,
                    'end': end,
                    'width': width,
                    'title': ''
                })

            data.close()
            self.total = len(self.levels)

    def getLevel(self, index):
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
        if self.current < self.total:
            self.current += 1
            return self.getLevel(self.current)

        return False

    def showLevelsFiles(self, direction):
        if direction == 'up':
            if self.fileSelected > 0:
                self.fileSelected -= 1
            else:
                self.fileSelected = len(self.listLevelsFiles) - 1

        elif direction == 'down':
            if self.fileSelected < len(self.listLevelsFiles) - 1:
                self.fileSelected += 1
            else:
                self.fileSelected = 0

        return self.listLevelsFiles[self.fileSelected]

    def reset(self):
        self.fileSelected = 0
        self.levels = []
        self.levelsFile = None
        self.total = 0
        self.current = 0

    def genBackground(self):
        for y in range(22):
            for x in range(30):
                rand = pyxel.rndi(1, 20)
                if rand < 6:
                    pyxel.tilemaps[1].pset(x, y, (10, 1))
                elif rand >= 6 and rand < 10:
                    pyxel.tilemaps[1].pset(x, y, (9, 1))
                elif rand >= 10 and rand < 14:
                    pyxel.tilemaps[1].pset(x, y, (11, 1))
                elif rand >= 14 and rand < 17:
                    pyxel.tilemaps[1].pset(x, y, (12, 1))
                else:
                    pyxel.tilemaps[1].pset(x, y, (13, 1))
