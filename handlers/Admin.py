from google.appengine.ext.ndb import Key

from Authentication import *
from config import app_config
from models.AdminAccount import AdminAccount
from models.MoneyUsage import MoneyUsage
from models.Month import Month
from models.Person import Person


class AdminHandler(Handler):
    def get(self):
        if not is_login(self):
            self.response.set_cookie("redirect", "/admin")
            self.redirect("/admin/login")
        else:
            self.render("admin.html",
                        app_name=app_config["app-name"],
                        account=AdminAccount.get(),
                        people=Person.get_all())

    def post(self):
        if not is_login(self):
            self.response.status = 401
            self.write("Please login to perform this action!")
        else:
            action = self.request.get("action")
            actions = {
                "changepassword": self.change_password,
                "getpersoninfo": self.get_person_info,
            }
            method = actions.get(action, None)
            if method:
                method()
            else:
                self.response.status = 409
                self.write("Invalid action.")

    def change_password(self):
        password = self.request.get("password")
        strength = AdminAccount.calculate_password_strength(password)

        if strength == -1:
            self.response.status = 409
            self.write("Password must not contain non-ASCII characters")
        elif strength == 0:
            self.response.status = 409
            self.write("Password must not be empty")
        elif strength < 9:
            self.response.status = 409
            self.write("Password is too weak")
        else:
            # update data store
            account = AdminAccount.get()
            account.salt = account.create_salt()
            account.hashed_password = account.hash(password, account.salt)
            account.put()

            # set login cookie
            self.write(account.hashed_password)

    def get_person_info(self):
        try:
            key = Key(urlsafe=self.request.get("key"))
            person = key.get()

            # get total spend
            months = list(Month.query().filter(Month.people == key).fetch())
            total_spend = sum(month.average for month in months) * 1000

            # get payments made for every one
            money_usages = list(MoneyUsage.query().filter(MoneyUsage.person == key).fetch())
            payment = sum(money_usage.money_spend for money_usage in money_usages) * 1000

            # last month
            last_money_usage = person.last_money_usage.get()
            last_month = last_money_usage.month.get()
            last_month_str = last_month.to_string_short() + " (" + last_month.to_string_long() + ")"

            print(last_month.key)
            print(Month.get_current_month_key())

            # write
            s = ";".join(map(str, [person.name, key.urlsafe(), total_spend, len(months), payment, last_month_str,
                                   last_money_usage.next_month_left * 1000,
                                   last_month.key == Month.get_current_month_key()]))
            self.write(s)

        except Exception as e:
            print(e)
            self.response.status = 409
            self.write("Can not resolve this buyer's key. Please reload this page and try again later")
