from . import Command
from .. import settings


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

