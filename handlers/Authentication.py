from BaseHandler import Handler
from models.AdminAccount import AdminAccount


def is_login(handler):
    """Check if user has the right login cookie"""
    # login cookie has the value of the hashed password
    return AdminAccount.get().hashed_password == handler.request.cookies.get("login", "")


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
            admin_account = AdminAccount.get()

            if not admin_account.validate_password(password):
                self.render("login.html", error="Wrong password")
            else:
                redirect_page = self.request.cookies.get("redirect", "/admin")
                print(">>>>>>>")
                print(redirect_page)
                self.response.delete_cookie("redirect")
                # login cookie has the value of the hashed password
                self.response.set_cookie("login", admin_account.hashed_password)
                self.redirect(redirect_page)


class Logout(Handler):
    """Remove login cookie"""

    def get(self):
        self.response.delete_cookie("login")
        self.response.delete_cookie("redirect")
        self.redirect("/")

    def post(self):
        self.response.delete_cookie("login")
        self.response.delete_cookie("redirect")
        self.redirect("/")
