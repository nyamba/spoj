import requests, getpass, cookielib
from requests.cookies import RequestsCookieJar
from . import settings


class Command(object):

    def __init__(self, name, desc):
        self.name = name
        self.desc = desc

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
        name = None

        while loop:
            if name is None:
                if settings.username:
                    name = settings.user_name
                    print 'loaded user name from config, [%s]' % name
                else:
                    name = raw_input('user name:')

            passw = getpass.getpass()

            payload = dict(login_user=name, password=passw,
                    autologin=1, submit='Log In')

            r = self.post(settings.LOGIN_URL, data=payload)
            if self.is_authenticated():
                print 'Welcome %s to %s!' % (name, settings.SPOJ_URL)
                loop = False
            else:
                print 'incorrect user name or password! Try again.'
                name = settings.user_name

    def get(self, url, data=None, **kwargs):
        return self.requests.get(url, data, **kwargs)

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
        parser.add_argument('user_name')


class UserStatus(Command):

    def __init__(self):
        super(UserStatus, self).__init__('status',
                'show user status of current or specied',
                )

    def doing(self, args):
        print args.user_name

    def add_arguments(self, parser):
        parser.add_argument('user_name')
