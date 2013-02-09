# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
from . import Command
from ..settings import _url
from ..utils import unescape as _, pager, escape_sub


class ProblemDesc(Command):
    def __init__(self):
        super(ProblemDesc, self).__init__('desc',
                'describe a problem')

    def add_arguments(self, parser):
        parser.add_argument('problem_id')
        parser.add_argument('--input', action='store_true',
                help='only give example input')
        parser.add_argument('--output', action='store_true',
                help='only give example output')

    def doing(self, args):
        __, soup = self.get_soup(_url('problems/'+args.problem_id))

        title = '%s <%s>' % (_(soup.findAll('h1')[1].text), args.problem_id)
        pp = soup.findAll('p')
        desc = BeautifulSoup(escape_sub(_(str(pp[1])))).text
        if desc.endswith('Input'):
            desc = desc[:-5]
        inp = _(pp[2].text)
        if inp.endswith('Output'):
            inp = inp[:-6]
        out = _(pp[3].text)
        idx = out.find('ExampleInput:')
        if idx:
            out = out[:idx]

        example = _(soup.find('pre').text)
        idx = example.find('Output:')
        _in = example[6:idx]
        _out = example[idx+7:]

        content = '\n** %s **\n%s\n\n'
        content += 'input:\n%s\n---------------\n%s\n\n'
        content += 'output:\n%s\n---------------\n%s'
        content = content % (title, desc, inp, _in, out, _out)

        if args.input:
            content = _in
        if args.output:
            content =  _out

        pager(content)
