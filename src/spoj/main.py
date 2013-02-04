import logging, argparse, ConfigParser, cookielib

from .commands import ProblemList, UserStatus, Authenticate
from . import settings


def parseConfig():
    cfg = ConfigParser.ConfigParser()
    cfg.read([settings.CONFIG_FILE_NAME])
    for (k, v) in cfg.items('user'):
        logging.info('loaded config: %s=%s' % (k, v))
        setattr(settings, k, v)

    try:
        cj = cookielib.MozillaCookieJar(settings.COOKIE_FILE_NAME)
        cj.load()
        cj.clear_expired_cookies()
        settings.cj = cj
    except:
        settings.cj = cookielib.MozillaCookieJar()
        logging.info('don\'t have existing cookie')


def _getOptionsParser():
    _commands = [
         Authenticate(),
         ProblemList(),
         UserStatus(),
         ]

    parser = argparse.ArgumentParser(prog='spoj', description='command line \
    tool for spoj.com')
    sub_parsers = parser.add_subparsers()

    for c in _commands:
        _parser = sub_parsers.add_parser(c.name, help=c.desc)
        c.add_arguments(_parser)

        _parser.set_defaults(func=c.do)

    return parser


def runner():
    parseConfig()
    parser = _getOptionsParser()
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    runner()
