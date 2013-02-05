# -*- coding: utf-8 -*-
from . import Command
from . import settings
from ..settings import _url
from ..utils import unescape as _


LANG_EXT = {
        'py':    {'python 2.7':4, 'python 3.2.3':116},
        'rb':    {'ruby 1.9.3': 17},
        'php':   {'php 5.2.6': 29},
        'java':  {'java SE 6': 10},
        'jar':   {'java SE 6': 24},
        'pas':   {'fpc 2.2.4': 22, 'gpc 20070904': 2},
        'pl':    {'perl 5.12.1': 3},
        'scala': {'scala 2.8.0': 39},
        'sed':   {'sed 4.2': 46},
        'c':     {'gcc 4.3.2': 11},
        'cpp':   {'g++ 4.3.2': 41, 'g++ 4.0.0-8':1},
        'cs':    {'gmcs 2.0.1': 27},
        'asm':   {'nasm 2.03.01': 13},
        'go':    {'gc 2010-07-14': 114},
        'sh':    {'bash 4.0.37': 104},
        }


class TackleProblem(Command):
    def __init__(self):
        super(TackleProblem, self).__init__('tackle',
                'upload a solution to %s' % settings.ROOM_URL())

    def add_arguments(self, parser):
        parser.add_argument('file_name')

    def doing(self):
        pass
