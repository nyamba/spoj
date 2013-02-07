# -*- coding: utf-8 -*-
import sys, time
from . import Command
from . import settings
from ..settings import _url
from ..utils import unescape as _


LANG_COMP = {
        'py':    {4: 'python 2.7', 116: 'python 3.2.3'},
        'rb':    {17: 'ruby 1.9.3'},
        'php':   {29: 'php 5.2.6'},
        'java':  {10: 'java SE 6'},
        'jar':   {24: 'java SE 6'},
        'pas':   {22: 'fpc 2.2.4', 2: 'gpc 20070904'},
        'pl':    {3: 'perl 5.12.1'},
        'scala': {39: 'scala 2.8.0'},
        'sed':   {46: 'sed 4.2'},
        'c':     {11: 'gcc 4.3.2'},
        'cpp':   {41: 'g++ 4.3.2', 1: 'g++ 4.0.0-8'},
        'cs':    {27: 'gmcs 2.0.1'},
        'asm':   {13: 'nasm 2.03.01'},
        'go':    {114: 'gc 2010-07-14'},
        'sh':    {104: 'bash 4.0.37'},
        }


class TackleProblem(Command):
    def __init__(self):
        super(TackleProblem, self).__init__('tackle',
                'upload a solution to %s' % settings.ROOM_URL())
        self.wait_time = 5

    def add_arguments(self, parser):
        parser.add_argument('file_name', help='file_name must be formatted \
                like this: <problem_id>.<lang_extention>\n for example: \
                ABR0001.py')

    def doing(self, args):
        if settings.compiler_id:
            cmp_id = int(settings.compiler_id)
            print 'compiler id loaded from settings: %d' % cmp_id
        else:
            cmp_id, cmp_name = self.get_compiler(args.file_name)
            print 'Your solution will be compiled via %s(%d)' % (cmp_name,
            cmp_id)

        self.auth_if()
        problem_id = args.file_name.split('.')[0]
        url = _url('submit/complete')
        files = {'subm_file': (args.file_name, open(args.file_name, 'r'))}
        r = self.post(url,
                data={'lang':cmp_id,
                    'problemcode':problem_id,
                    'file': '',
                    'submit': 'submit',
                    },
                files=files)
        loop = True
        while loop:
            print 'waiting result for %d seconds!' % self.wait_time
            time.sleep(self.wait_time)
            print '\n **result** \n'
            result = self.get_result(problem_id)
            print 'date: %s\nname: %s\nstatus: %s\ntime: %s\nmemory: %s' %\
                    result
            if u'байна' not in result[2]:
                loop = False
            else:
                print 'fetching result again, ',


    def get_compiler(self, file_name):
        ext = file_name.split('.')[-1]
        compilers = LANG_COMP.get(ext, {})
        compiler_id = -1
        compiler_name = ''

        if len(compilers) == 0:
            raise ValueError('oops, don\'t have a compiler for your file')
        elif len(compilers) > 1:
            print 'there are many compilers,',
            while True:
                print 'please choose one of followings:'
                for k, v in compilers.iteritems():
                    print '%3d: %s' % (k, v)
                try:
                    compiler_id = input()
                    compiler_name = compilers[compiler_id]
                    break
                except:
                    print 'invalid!, only choose one id of provided'
        else:
            compiler_id, compiler_name = compilers.iteritems()[0]

        return compiler_id, compiler_name

    def get_result(self, problem_id):
        '''
        return last result of the problem
        '''
        url = _url('status/%s,%s' % (problem_id, settings.user_name))
        __, soup = self.get_soup(url)
        rows = soup.findAll('table', {'class': 'problems'})[1].\
                findAll('tr')[1].findAll('td')
        date = rows[2].text
        name = _(rows[3].text)
        status = _(rows[4].text)
        status = status.replace('edit', '')
        status = status.replace('run', '')
        time = rows[5].find('a').text
        mem = rows[6].text

        return (date, name, status, time, mem)
