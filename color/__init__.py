from contextlib import contextmanager

import builtins
import sys

__all__ = ['print']

# There's quite a bit of setup for windows, but oh well.
if sys.platform == 'win32':
    from ctypes import windll, Structure, byref
    from ctypes import c_ushort as ushort, c_short as short

    class Coord(Structure):
        _fields_ = [('x', short), ('y', short)]

    class SmallRect(Structure):
        _fields_ = [(x, short) for x in ('left', 'top', 'right', 'bottom')]

    class ConsoleScreenBufferInfo(Structure):
        _fields_ = [
            ('size', Coord),
            ('cursor_position', Coord),
            ('attributes', ushort),
            ('window', SmallRect),
            ('maximum_window_size', Coord)
        ]

    # STDOUT and STDERR use the same attributes
    __handle = windll.kernel32.GetStdHandle(-11)

    def __get_console():
        csbi = ConsoleScreenBufferInfo()
        windll.kernel32.GetConsoleScreenBufferInfo(__handle, byref(csbi))
        return csbi.attributes

    set_console = windll.kernel32.SetConsoleTextAttribute
    default_colors = __get_console()

__windows = sys.platform == 'win32'
__win32 = [color | 0x8 & 0xFF0F for color in [0, 4, 2, 6, 1, 5, 3, 7]]
__names = 'grey', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'
__colors = dict(zip(__names, __win32 if __windows else range(8)))

def print(*args, **kwargs):
    if 'color' not in kwargs:
        builtins.print(*args, **kwargs)
        return

    color = kwargs['color']
    if color not in __colors: 
        raise AttributeError('invalid color: {}'.format(color))

    color = __colors[kwargs['color']]
    file = kwargs.get('file', sys.stdout)
    sep = kwargs.get('sep', ' ')
    end = kwargs.get('end', '\n')

    with __setup_color(color, file):
        builtins.print(*args, sep=sep, end=end, file=file)

@contextmanager
def __setup_color(color, file):
    if __windows: set_console(__handle, color)
    else: builtins.print('\33[1;3{}m'.format(color), end='', file=file)
    yield
    if __windows: set_console(__handle, default_colors)
    else: builtins.print('\33[0m', end='', file=file)
