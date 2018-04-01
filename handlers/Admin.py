from google.appengine.ext import ndb
from google.appengine.ext.ndb import Key

from Authentication import *
from config import app_config
from libs.validate_email import validate_email
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
                        people=Person.get_all(),
                        months=Month.get_all(),
                        )

    def post(self):
        if not is_login(self):
            self.response.status = 401
            self.write("Please login to perform this action!")
        else:
            action = self.request.get("action")
            actions = {
                "changepassword": self.change_password,
                "getpersoninfo": self.get_person_info,
                "newperson": self.new_person,
                "getmonthinfo": self.get_month_info,
                "listitems": self.list_items,
                "deleteitems": self.delete_items,
                "deleteemail": self.delete_email,
                "createemail": self.create_email,
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
            if person.last_money_usage:
                last_money_usage = person.last_money_usage.get()
                last_month = last_money_usage.month.get()

                last_month_str = last_month.to_string_long()
                next_month_left = last_money_usage.next_month_left * 1000
                in_current_month = last_month.key == Month.get_current_month_key()
            else:
                last_month_str = next_month_left = in_current_month = "N/A"

            # write
            s = ";".join(map(unicode, [person.name, key.id(), total_spend, len(months), payment,
                                       last_month_str, next_month_left, in_current_month]))
            self.write(s)

        except Exception as e:
            print(e)
            self.response.status = 409
            self.write("Can not resolve this buyer's key. Please reload this page or try again later")

    def new_person(self):
        name = self.request.get("name")
        if not Person.validate_name(name):
            self.response.status = 409
            self.write(
                "Invalid name. A valid name must be unique, between 1 and 20 letters "
                "and must not contains punctuations (except the '_')")
        else:
            person = Person(name=name)
            person.put()
            self.write(";".join([person.key.urlsafe(), person.name]))

    def get_month_info(self):
        try:
            month = Key(urlsafe=self.request.get("key")).get()
            prev_month = month.prev_month.get().to_string_short() if month.prev_month else "N/A"
            next_month = month.next_month.get().to_string_short() if month.next_month else "N/A"
            people_in_month = ", ".join([person.get().name for person in month.people])

            # write
            s = ";".join(map(unicode, [
                month.to_string_short(),
                month.time_begin_format(),
                month.time_end_format(),
                prev_month,
                next_month,
                people_in_month,
                month.spend,
                month.average,
                month.key.urlsafe(),
            ]))
            self.write(s)

        except Exception as e:
            print(e)
            self.response.status = 409
            self.write("Can not resolve this month's key. Please reload this page or try again later")

    def list_items(self):
        try:
            month = Key(urlsafe=self.request.get("key")).get()
            people = ndb.get_multi(month.people)
            key_to_people = {person.key: person for person in people}

            items = []
            for item in month.items:
                items.append("|".join([
                    item.date.strftime("%d/%m/%y"),
                    key_to_people[item.buyer].name,
                    item.what,
                    str(item.price)
                ]))

            # write
            s = ";".join([month.key.urlsafe()] + items)
            self.write(s)

        except Exception as e:
            print(e)
            self.response.status = 409
            self.write("Can not list items in this month. Please reload this page or try again later")

    def delete_items(self):
        try:
            month = Key(urlsafe=self.request.get("key")).get()
            items_to_del = set(map(int, self.request.get("items").split(",")))

            items = [month.items[i] for i in set(range(len(month.items))) - items_to_del]

            month.items = items
            month.update_chain()

            # write
            self.write(month.key.urlsafe())

        except Exception as e:
            print(e)
            self.response.status = 409
            self.write("Can not delete item(s) in this month. Please reload this page or try again later")

    def delete_email(self):
        email = self.request.get("email")
        account = AdminAccount.get()
        try:
            account.emails.remove(email)
        except ValueError:
            self.response.status = 409
            self.write("Email does not exist!")
        else:
            account.put()
            self.write(email)

    def create_email(self):
        email = self.request.get("email")
        if validate_email(email):
            account = AdminAccount.get()
            if email not in account.emails:
                account.emails.append(email)
                account.put()
                self.write(email)
            else:
                self.response.status = 409
                self.write("Email has already exists!")
        else:
            self.response.status = 409
            self.write("Invalid email!")
