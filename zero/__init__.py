"""
Zero  
A new Python documentation style

Author
------
Animenosekai
    Original author
"""

from zero.zero import Function, Docs


__version_tuple__ = (1, 0, '(beta)')


def __version_string__():
    if isinstance(__version_tuple__[-1], str):
        return '.'.join(map(str, __version_tuple__[:-1])) + __version_tuple__[-1]
    return '.'.join(str(i) for i in __version_tuple__)


__author__ = 'Anime no Sekai'
__copyright__ = 'Copyright 2022, zero'
__credits__ = ['animenosekai']
__license__ = 'MIT License'
__version__ = 'zero v{}'.format(__version_string__())
__maintainer__ = 'Anime no Sekai'
__email__ = 'niichannomail@gmail.com'
__status__ = 'Stable'
