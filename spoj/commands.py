# -*- coding: utf-8 -*-
import requests, getpass, cookielib, argparse
from BeautifulSoup import BeautifulSoup
from requests.cookies import RequestsCookieJar
from . import settings
from .settings import _url
from .utils import unescape as _


class Command(object):

    def __init__(self, name, desc):
        self.name = name
        self.desc = desc
        self._session = None

    def save_cookies(self):
        mcj = cookielib.MozillaCookieJar(settings.COOKIE_FILE_NAME)
        [mcj.set_cookie(c) for c in self._session.cookies]
        mcj.save()

    def do(self, args):
        self.doing(args)
        self.save_cookies()

    def doing(self, args):
        '''
        chilren should implement it
        '''
        raise NotImplemented()

    def getHTTPClient(self):
        if self._session:
            return self._session

        rcj = RequestsCookieJar()
        for c in settings.cj:
            rcj.set_cookie(c)

        self._session = requests.Session()
        self._session.cookies = rcj

        return self._session

    def is_authenticated(self):
        try:
            assert self.requests.cookies['autologin_hash']
            assert self.requests.cookies['autologin_login']
            return True
        except:
            return False

    def auth_if(self):
        if not self.is_authenticated():
            self.authenticate()

    def __getattribute__(self, name):
        if name == 'requests':
            return self.getHTTPClient()
        else:
            return super(Command, self).__getattribute__(name)

    def add_arguments(self, parser):
        pass

    def authenticate(self):
        loop = True
        print 'Authenticating user for ' + settings.SPOJ_URL

        self.requests.cookies.clear()

        while loop:
            name = settings.user_name
            if name is None:
                if settings.user_name:
                    name = settings.user_name
                    print 'loaded user name from config, [%s]' % name
                else:
                    name = raw_input('user name:')

            passw = getpass.getpass()

            payload = dict(login_user=name, password=passw,
                    autologin=1, submit='Log In')

            r = self.post(settings.LOGIN_URL, data=payload)
            if self.is_authenticated():
                print 'Welcome %s to %s' % (name, settings.SPOJ_URL)
                loop = False
            else:
                print 'incorrect user name or password! Try again.'

    def get(self, url, **kwargs):
        return self.requests.get(url, **kwargs)

    def post(self, url, data=None, **kwargs):
        return self.requests.post(url, data, **kwargs)


class ProblemList(Command):

    def __init__(self):
        super(ProblemList, self).__init__('problems',
                'problem list')

    def do(self, args):
        print args


class Authenticate(Command):
    def __init__(self):
        super(Authenticate, self).__init__('login',
                'Authenticate user to the app')

    def doing(self, args):
        if args.user_name:
            settings.user_name = args.user_name

        self.authenticate()

    def add_arguments(self, parser):
        parser.add_argument('user_name', nargs='?')


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

        r = self.get(_url(path))
        soup = BeautifulSoup(r.text)
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
