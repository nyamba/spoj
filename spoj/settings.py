import os

SPOJ_URL = 'http://www.spoj.com/'
LOGIN_URL = SPOJ_URL
MN_SPOJ_URL = '%sABRAMOV/' % SPOJ_URL

CONFIG_FILE_NAME = os.path.expanduser('~/.spojrc')
COOKIE_FILE_NAME = os.path.expanduser('~/.spoj_cookie')

user_name = None
#cookie jar
cj = None

def _url(path):
    return MN_SPOJ_URL + path + '/'
