from Authentication import *
from config import app_config
from models.AdminAccount import AdminAccount


class AdminHandler(Handler):
    def get(self):
        if not is_login(self):
            self.response.set_cookie("redirect", "/admin")
            self.redirect("/admin/login")
        else:
            self.render("admin.html",
                        app_name=app_config["app-name"],
                        account=AdminAccount.get())

    def post(self):
        if not is_login(self):
            self.response.status = 401
            self.write("Please login to perform this action!")
        else:
            action = self.request.get("action")
            actions = {
                "changepassword": self.change_password
            }
            method = actions.get(action, None)
            if method:
                method()
            else:
                self.response.status = 409
                self.write("Invalid action.")

    def change_password(self):
        # update data store
        password = self.request.get("password")
        account = AdminAccount.get()
        account.salt = account.create_salt()
        account.hashed_password = account.hash(password, account.salt)
        account.put()

        # set login cookie
        self.write(account.hashed_password)
