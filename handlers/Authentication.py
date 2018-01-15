import random
import string

import webapp2

from BaseHandler import Handler
from config import app_config

SECRET_COOKIE = app_config["login-cookie"]


def create_login_cookie():
    """Used to create secret cookie in app_config"""
    s = string.ascii_letters + string.digits + string.punctuation
    length = 25
    return "".join([random.choice(s) for _ in xrange(length)])


def is_login(handler):
    """Check if user has the right login cookie"""
    return handler.request.cookies.get("login", "") == SECRET_COOKIE


class Login(Handler):
    """Serve login page and handle login request"""

    def get(self):
        if is_login(self):
            self.render("login_success.html")
        else:
            self.render("login.html")

    def post(self):
        if is_login(self):
            self.render("login_success.html")
        else:
            password = self.request.get("password")
            if password != webapp2.get_app().config["login-password"]:
                self.render("login.html", error="Wrong password")
            else:
                redirect_page = self.request.cookies.get("redirect", "/admin/login")
                self.response.delete_cookie("redirect")
                self.response.set_cookie("login", SECRET_COOKIE)
                self.redirect(redirect_page)


class Logout(Handler):
    """Remove login cookie"""

    def get(self):
        self.response.delete_cookie("login")
        self.redirect("/")

    def post(self):
        self.response.delete_cookie("login")
        self.redirect("/")
