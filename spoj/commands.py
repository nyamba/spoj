from . import api


# `login` command.
#
#     > spoj login
#     Username: username
#     Password: ********
#
# - clear cookies
# - post request to login page (cookie automatically saved)
def login():
    api.clear_cookies()

    data = dict(autologin=1, submit="Log in")
    while True:
        data["login_user"] = api.input("username", "Username: ")
        data["password"]   = api.input("password", "Password: ")

        r = api.post(api.LOGIN_URL, data=data)
        if "autologin_login" in r.cookies:
            break
        print "\nLogin unsuccessful!\nUsername or password invalid!"

    print "Welcome!"


'''
@login_required
def problem():
    pass


@login_required
def submit():
    pass


`logout` command
def logout():
    # get request to http://www.spoj.com/logout
    pass
'''
