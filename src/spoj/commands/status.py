# -*- coding: utf-8 -*-
from . import Command
from ..settings import _url
from ..utils import unescape as _


class UserStatus(Command):

    def __init__(self):
        super(UserStatus, self).__init__('status',
                'show user status of current or specied',
                )

    def doing(self, args):
        if args.user_name:
            path = 'users/' + args.user_name
        else:
            path = 'myaccount'
            self.auth_if()

        __, soup = self.get_soup(_url(path))
        title = _(soup.find('h3').text)
        solved_list = filter(None, [a.text for a in
            soup.findAll('table')[4].findAll('a')])
        unsolved_list = filter(None, [a.text for a in
            soup.findAll('table')[5].findAll('a')])

        print '%s\n' % title
        print '%d бодлого бүрэн бодсон:' % len(solved_list)
        print ', '.join(solved_list)
        print '%d бодлого дутуу бодсон:' % len(unsolved_list)
        print ', '.join(unsolved_list)

    def add_arguments(self, parser):
        parser.add_argument('user_name', nargs='?')
