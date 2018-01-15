from Authentication import *


class AdminHandler(Handler):
    def get(self):
        if not is_login(self):
            self.response.set_cookie("redirect", "/admin")
            self.redirect("/admin/login")
        else:
            self.render("admin.html")

    def post(self):
        if not is_login(self):
            self.error(401)
        else:
            pass
