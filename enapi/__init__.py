import os

__version__ = '0.1.0'
__license__ = 'GPL2'
__author__ = 'Bernd Strebel'

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))

from .client import EnClient
from .notes import EnBook, EnNote, EnStack
from .enml import ENMLOfPlainText, PlainTextOfENML

__all__ = [

    'EnClient',
    'EnBook',
    'EnNote',
    'EnStack',
    'ENMLOfPlainText',
    'PlainTextOfENML'
]
