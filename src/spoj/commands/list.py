# -*- coding: utf-8 -*-
from prettytable import PrettyTable
from . import Command
from . import settings
from ..settings import _url
from ..utils import unescape as _, text_table, pager


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
        headers = []
        headers.append('Solution id(5)')
        if self.is_authenticated():
            headers.append('Solved(4)')
        headers.append('Problem name(1)')
        headers.append('Problem id(2)')
        headers.append('Users(6)')
        headers.append('Success(7)')

        total_col = len(headers)
        def cell_formatter(r, c, data_soup):
            if total_col > 5 and c == 1:
                return '*' if data_soup.find('img') else ''
            else:
                return _(data_soup.text)

        t = PrettyTable(headers)
        t.align["Problem name(1)"] = 'l'
        t.padding_with = 1

        table = soup.findAll('table',{'class': 'problems'})[-1]
        t = text_table(table, t, 1, cell_formatter)
        pager(t.get_string())

    def add_arguments(self, parser):
        choices, cc = [], [1, 2, 4, 5, 6, 7]
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
