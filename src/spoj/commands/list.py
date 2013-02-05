# -*- coding: utf-8 -*-
from . import Command
from . import settings
from ..settings import _url
from ..utils import unescape as _


class ProblemList(Command):
    def __init__(self):
        super(ProblemList, self).__init__('list',
                'list all problems on %s' % settings.ROOM_URL())

    def doing(self, args):
        arguments = []
        if args.sort:
            arguments.append('sort=%d' % args.sort)
        if args.page:
            arguments.append('start=%d' % args.page)

        url = _url('problems/main') + ','.join(arguments)

        __, soup = self.get_soup(url)
        t = PrettyTable(['Solution id(5)', 'Problem name(1)',
            'Problem id(1)', 'Candidates(6)', 'Success(7)'])
        t.align["Problem name(1)"] = 'l'
        t.padding_with = 1

        table = soup.find('table',{'class': 'problems'})
        t = text_table(table, t, 1)
        pager(t.get_string())

    def add_arguments(self, parser):
        choices, cc = [], [1, 2, 5, 6, 7]
        for c in cc:
            choices.append(c)
            choices.append(-c)
        parser.add_argument('--page', type=int, nargs='?',
                help='page number of problem list page')
        parser.add_argument('--sort', type=int, choices=choices, nargs='?',
                help='''column number which will be sorted, if it is positive,
                ascending order else descending, available options:
                    1 - problem id,
                    2 - problem name,
                    5 - solution id,
                    6 - users count who solved it,
                    7 - percentage of valid solutions
                ''')
