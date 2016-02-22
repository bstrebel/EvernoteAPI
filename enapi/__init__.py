import os

__version__ = '0.2.4'
__license__ = 'GPL2'
__author__ = 'Bernd Strebel'

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))

from .client import EnClient
from .notes import EnBook, EnNote, EnStack
from .enml import ENMLOfPlainText, PlainTextOfENML, HTMLOfENML

__all__ = [

    'EnClient',
    'EnBook',
    'EnNote',
    'EnStack',
    'ENMLOfPlainText',
    'PlainTextOfENML',
    'HTMLOfENML'
]
