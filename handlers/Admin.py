from Authentication import *
from config import app_config


class AdminHandler(Handler):
    def get(self):
        if not is_login(self):
            self.response.set_cookie("redirect", "/admin")
            self.redirect("/admin/login")
        else:
            self.render("admin.html", app_name=app_config["app-name"])

    def post(self):
        if not is_login(self):
            self.error(401)
        else:
            pass
