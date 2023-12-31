from math import floor
from os import listdir, path
import pathlib


__dir = pathlib.Path(__file__).parent.resolve()
LEVELS_DIR = path.join(__dir, 'levels')


class Levels:
    def __init__(self):
        self.listLevelsFiles = []
        self.fileSelected = 0
        self.levels = []
        self.levelsFile = None
        self.total = 0
        self.current = 0

        for f in sorted(listdir(LEVELS_DIR)):
            self.listLevelsFiles.append(f)

    def loadLevels(self):
        self.levelsFile = self.listLevelsFiles[self.fileSelected]
        self.total = 0
        self.current = 0

        with open(path.join(LEVELS_DIR, self.levelsFile)) as data:
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
                                'start':    levelStartLine,
                                'end':      i,
                                'width':    width
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

                ''' elif not levelEnd:
                    print(lastLine)
                    end = i if '#' in lastLine else i - 1
                    self.levels.append({
                        'start':    levelStartLine,
                        'end':      end,
                        'width':    width
                    })
                    levelEnd = True
                    width = 0'''

            if not levelEnd:

                end = totalLines if '#' in lastLine else totalLines - 1
                self.levels.append({
                    'start':    levelStartLine,
                    'end':      end,
                    'width':    width
                })

            data.close()
            self.total = len(self.levels)

    def getLevel(self, index):
        level = self.levels[index]
        lines = []
        with open(path.join(LEVELS_DIR, self.levelsFile)) as f:
            for fline in f.readlines()[level['start']:level['end']]:
                line = []
                for i in range(level['width']):
                    line.append('')

                for i, char in enumerate(fline.replace('\n', '')):
                    line[i] = char

                lines.append(line)
            f.close()

        width = level['width']
        height = level['end'] - level['start']

        start_x = floor(((30 - width) / 2) - 1)
        start_y = floor(((17 - height) / 2) - 1)

        return {
            'width':    width,
            'height':   height,
            'lines':    lines,
            'start_x':  start_x,
            'start_y':  start_y
        }

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
