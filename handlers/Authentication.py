from datetime import datetime, timedelta

from google.appengine.api import mail

from BaseHandler import Handler
from config import app_config
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
                self.response.delete_cookie("redirect")
                # login cookie has the value of the hashed password
                if self.request.get("remember"):
                    expire_date = datetime.now() + timedelta(30)
                else:
                    expire_date = None
                self.response.set_cookie("login", admin_account.hashed_password, expires=expire_date)
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


class RecoverPassword(Handler):
    def post(self):
        email = self.request.get("email")
        if email not in AdminAccount.get().emails:
            self.response.status = 409
            self.write("This email is not registered as an email of admin")
        else:
            try:
                new_password = AdminAccount.set_new_random_password()
                app_name = app_config["app-name"]
                html_content = self.render_str("recover-password-email.html",
                                               new_password=new_password,
                                               app_name=app_name)

                email_message = mail.EmailMessage(
                    sender="recover_password@{}.appspotmail.com".format(app_name),
                    to=email,
                    subject="Recover password",
                    html=html_content
                )

                email_message.send()
            except Exception as e:
                print(e)
                self.response.status = 500
                self.write("An error occurred while the server was trying to send you email. Please try again later.")
            else:
                self.write("An email has been send to you. Please check mail and follow the instructions.")
