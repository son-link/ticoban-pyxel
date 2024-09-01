import pyxel


class PyxelMenu:
    """ Pyxel class for generating, displaying and controlling a menu """

    def __init__(self, x: int, y: int, options: list = None, limit: int = 5):
        """Class constructor

        Args:
            x (int): Position of the menu with respect to the left margin in pixels
            y (int): Position of the menu with respect to the up margin in pixels
            options (list): A list with the options to add. Defaults to None
            limit (int, optional): The limit of options to display. Defaults to 5.
        """
        self._limit = limit
        if options and len(options) < limit:
            self._limit == len(options)

        self._x = x
        self._y = y
        self._current_pos = 0
        self._cursor = {
            'type': 'circle',
            'color': 7
        }
        self._color = 7
        self._cursor_color = 7
        self._cursor_img = {
            'use': False,
            'img': 0,
            'u': 0,
            'v': 0,
            'colkey': None
        }
        self._highlight = {
            'use': False,
            'color': 7
        }
        self._options = options

    def draw(self):
        ''' Draw the menu '''
        if not self._options:
            return

        starty = self._y

        init = 0
        cursor_pos = self._current_pos
        middle = pyxel.floor(self._limit / 2)

        if (
            len(self._options) > self._limit and
            self._current_pos < len(self._options)
        ):
            if (
                self._current_pos > middle and
                self._current_pos < len(self._options) - middle
            ):
                init = self._current_pos - middle
                cursor_pos = middle
            elif (
                self._current_pos >= len(self._options) - pyxel.floor(self._limit / 2)
            ):
                init = len(self._options) - self._limit
                cursor_pos = self._current_pos - init

        for i, option in enumerate(self._options[init:init + self._limit]):
            text_color = self._color

            if i == cursor_pos:
                if self._cursor_img['use']:
                    pyxel.blt(
                        self._x,
                        starty,
                        self._cursor_img['img'],
                        self._cursor_img['u'],
                        self._cursor_img['v'],
                        8,
                        8,
                        self._cursor_img['colkey']
                    )
                else:
                    if self._cursor['type'] == 'circle':
                        pyxel.circ(self._x + 5, starty + 2, 2, self._cursor['color'])
                    elif self._cursor['type'] == 'triangle':
                        pyxel.tri(self._x + 2, starty, self._x + 2, starty + 4, self._x + 6, starty + 2, self._cursor['color'])
                    elif self._cursor['type'] == 'square':
                        pyxel.rect(self._x + 2, starty, 5, 5, self._cursor['color'])

                if self._highlight['use']:
                    text_color = self._highlight['color']

            pyxel.text(self._x + 10, starty, option, text_color)
            starty += 8

    def get_current_pos(self):
        ''' Return selected option index '''
        return self._current_pos

    def get_current_text(self):
        ''' Return selected option text '''
        return self._options[self._current_pos]

    def move_up(self):
        ''' Move the cursor up one position '''
        if self._current_pos > 0:
            self._current_pos -= 1

    def move_down(self):
        ''' Move the cursor down one position '''
        if self._current_pos < len(self._options) - 1:
            self._current_pos += 1

    def set_cursor(self, cursor_type: str = 'circle', color: int = 7):
        """Defines the type and/or color of the cursor to be used

        Args:
            cursor_type (str, optional): The type of the cursor (circle, square, triangle). Defaults to 'circle'.
            color (int, optional): The color index of the Pyxel palette to use for the options (0-15). Defaults to 7.
        """
        if (
            cursor_type and
            cursor_type == 'circle' or
            cursor_type == 'square' or
            cursor_type == 'triangle'
        ):
            self._cursor['type'] = cursor_type

        if color >= 0 and color <= 15:
            self._cursor['color'] = color

    def set_cursor_img(self, img: int, u: int, v: int, colkey: int = None):
        """Set an image from the image bank as the cursor.

        Args:
            img (int): The image bank (0-2) to use
            u (int): Horizontal image position
            v (int): Vertical image position
            colkey (int, optional): If a color is indicated, it will be considered as transparent. Defaults to None.
        """
        self._cursor_img = {
            'use': True,
            'img': img,
            'u': u,
            'v': v,
            'colkey': colkey
        }

    def set_cursor_pos(self, pos: int):
        ''' Set the current position of the cursor '''
        self._current_pos = pos

    def set_highlight_color(self, color: int):
        """Sets the highlight color for the indicated option.

        Args:
            color (int): The color index of the Pyxel palette to use for the options (0-15)
        """
        if color >= 0 and color <= 15:
            self._highlight['color'] = color
            self._highlight['use'] = True

    def set_options(self, options: list):
        """Set the options for the menu

        Args:
            options (list): The options list
        """
        self._options = options
        if len(self._options) < self._limit:
            self._limit == len(options)

    def set_text_color(self, color: int):
        """Defines the color of the options

        Args:
            color (int): The color index of the Pyxel palette to use for the options (0-15)
        """
        if color < 0 or color > 15:
            return

        self._color = color
