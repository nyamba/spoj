# -*- coding: utf-8 -*-
from . import Command
from ..settings import _url
from ..utils import unescape as _, pager


class ProblemDesc(Command):
    def __init__(self):
        super(ProblemDesc, self).__init__('desc',
                'describe a problem')

    def add_arguments(self, parser):
        parser.add_argument('problem_id')

    def doing(self, args):
        __, soup = self.get_soup(_url('problems/'+args.problem_id))

        title = '%s <%s>' % (_(soup.findAll('h1')[1].text), args.problem_id)
        pp = soup.findAll('p')
        desc = _(pp[1].text)
        inp = _(pp[2].text)
        out = _(pp[3].text)
        idx = out.find('ExampleInput:')
        if idx:
            out = out[:idx]

        desc = '\n** %s **\n\n %s \n\ninput:\n%s\nout:\n%s' % (title, desc, inp, out)

        pager(desc)
