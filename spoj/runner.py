import argparse
from . import commands

DESCRIPTION = "CLI client for spoj.com"


# _PUBLIC_: CLI bootstrapper
def bootstrap():
    parser = argparse.ArgumentParser(prog="spoj", description=DESCRIPTION)
    subparsers = parser.add_subparsers(help="commands")

    # A login command
    sub = subparsers.add_parser("login", help="Login to site")
    sub.set_defaults(func=commands.login)

    # A lorem command
    # sub = subparsers.add_parser("lorem", help="Lorem ipsum")
    # sub.set_defaults(func=commands.lorem)

    args = parser.parse_args()
    args.func()
