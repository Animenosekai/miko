"""Stores information on the current module version"""
# Authors
__author__ = 'Anime no Sekai'
__maintainer__ = 'Anime no Sekai'
__credits__ = ['animenosekai']
__email__ = 'animenosekai.mail@gmail.com'
__repository__ = 'https://github.com/Animenosekai/miko'
# Module
__module__ = 'Miko'
__status__ = 'Stable'
__year__ = 2023
__license__ = 'MIT License'
__copyright__ = f'Copyright {__year__}, {__module__}'
# PEP 440 Compilant
__version__ = '2.0'
import typing


def test(a: typing.Callable[[str, int], bool]):
    """
    Parameters
    ----------
    a: () -> Any | (str, int) -> bool

    Raises
    ------
    ValueError
    """
    try:
        raise SyntaxError('Hello world')
    except SyntaxError:
        pass
    raise ValueError('Hello world')
