Color
=====

Color is a (very) small module for Python 3.2 and later. It allows printing
colors to the console. It works on any ANSI terminal, and the Windows command
line. To use it, simply use the print function as you always have, however you
now have the option of passing ``color`` to it as well.

Example::

    >>> from color import print
    >>> print('hello', 'world!', color='blue')

Available colors are:

 * grey
 * red
 * green
 * yellow
 * blue
 * magenta
 * cyan
 * white

Color does not currently support modifying background colors.
