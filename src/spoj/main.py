import logging, argparse, ConfigParser, cookielib, os, pkgutil, inspect
import importlib

from . import settings
from . import commands
from .commands import Command


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
    command_classes = find_cmd_classes(commands)

    _commands = [CC() for CC in command_classes]
    parser = argparse.ArgumentParser(prog='spoj', description='command line \
    tool for spoj.com')
    sub_parsers = parser.add_subparsers()

    for c in _commands:
        _parser = sub_parsers.add_parser(c.name, help=c.desc)
        c.add_arguments(_parser)

        _parser.set_defaults(func=c.do)

    return parser


def find_cmd_classes(pkg):
    path = os.path.dirname(pkg.__file__)
    pkgs = [name for _, name, _ in\
        pkgutil.iter_modules([path])]
    cmd = []

    for p in pkgs:
        p_name = '.'.join([pkg.__name__, p])
        ppg = importlib.import_module(p_name)
        classes = inspect.getmembers(ppg, inspect.isclass)
        for n, c in classes:
            if Command in c.__bases__:
                cmd.append(c)

    return cmd


def runner():
    parseConfig()
    parser = _getOptionsParser()
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    runner()
