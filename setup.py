from setuptools import setup
import re

version = re.search(
    "^__version__\s*=\s*'(.*)'",
    open('enapi/__init__.py').read(),
    re.M).group(1)

setup(
    name='EvernoteAPI',
    version=version,
    packages=['enapi'],
    url='https://github.com/bstrebel/EvernoteAPI',
    license='GPL2',
    author='Bernd Strebel',
    author_email='b.strebel@digitec.de',
    description='Evernote API Wrapper',
    long_description=open('README.md').read(),
    install_requires=['evernote']
)
