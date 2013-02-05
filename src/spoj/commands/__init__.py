# -*- coding: utf-8 -*-
import requests, getpass, cookielib
from BeautifulSoup import BeautifulSoup
from requests.cookies import RequestsCookieJar
from .. import settings


class Command(object):

    def __init__(self, name, desc):
        self.name = name
        self.desc = desc
        self._session = None

    def save_cookies(self):
        mcj = cookielib.MozillaCookieJar(settings.COOKIE_FILE_NAME)
        [mcj.set_cookie(c) for c in self.getHTTPClient().cookies]
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

    def get_soup(self, url, **kwargs):
        r = self.get(url, **kwargs)
        soup = BeautifulSoup(r.text)
        return r, soup
