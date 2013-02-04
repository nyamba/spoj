import os, json, getpass, requests

# CONSTANTS
# ---------

BASE_URL  = "http://www.spoj.com/"
LOGIN_URL = BASE_URL
# CONTEST   = "ABRAMOV"

COOKIE_FILE = os.path.expanduser("~/.spojcookie")

# METHODS
# -------

# _PUBLIC_: send HTTP/GET request
#
# - load saved cookie
# - send post request with cookies
# - save cookie
#
# _return_ response object
def get(url, *args, **kwargs):
    r = requests.get(url, cookies=load_cookies(), *args, **kwargs)
    save_cookies(dict(r.cookies))

    return r


# _PUBLIC_: send HTTP/POST request
#
# - load saved cookie
# - send post request with cookies
# - save cookie
#
# _return_ response object
def post(url, *args, **kwargs):
    r = requests.post(url, cookies=load_cookies(), *args, **kwargs)
    save_cookies(dict(r.cookies))

    return r


# _PUBLIC_: get input from stdin (interactively)
#
# - auto detect and hide password input
#
# _return_ input string
def input(name, message=""):
    if "pass" in name.lower() or "pass" in message.lower():
        return getpass.getpass()
    return raw_input(message)


# _PUBLIC_: load cookies (serialize: json)
def load_cookies():
    try:
        return json.load(open(COOKIE_FILE, "r"))
    except IOError:
        save_cookies({})
        return json.load(open(COOKIE_FILE, "r"))


# _PUBLIC_: save cookies (serialize: json)
def save_cookies(data):
    return json.dump(data, open(COOKIE_FILE, "w+"))


# _PUBLIC_: clear cookies
def clear_cookies():
    return save_cookies({})
