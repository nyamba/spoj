import os

SPOJ_URL = 'http://www.spoj.com/'
LOGIN_URL = SPOJ_URL
spoj_dirname = 'ABRAMOV'
compiler_id = None

ROOM_URL = lambda : SPOJ_URL + spoj_dirname +'/'

CONFIG_FILE_NAME = os.path.expanduser('~/.spojrc')
COOKIE_FILE_NAME = os.path.expanduser('~/.spoj_cookie')

user_name = None
#cookie jar
cj = None

_url = lambda path: ROOM_URL() + path + '/'

def get_user_name():
    global user_name
    if user_name:
        return user_name

    user_name = raw_input('user name:')
    return user_name
