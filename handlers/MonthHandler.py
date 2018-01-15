import re

from google.appengine.ext import ndb
from google.appengine.ext.ndb import Key

import BaseHandler
from BaseHandler import Handler
from models import *


class MonthHandler(Handler):
    """Handle request for a particular month"""

    def get(self, month_key):
        """Get month info and render html"""
        try:
            month = Key(urlsafe=month_key).get()
            if month is None:
                raise ValueError
        except:
            self.error(404)
        else:
            self.render_month(month)

    def post(self, month_key):
        """Handle adding new item and end month"""
        action = self.request.get("action")

        # create new month
        if action == "ADD":
            self.add_item()
        # end month
        elif action == "END MONTH":
            month = Month.end_month()
            if month:
                self.redirect("/month/" + month.key.urlsafe())
        else:
            self.redirect("/home")

    def render_month(self, month, errors=None):
        """Render money_current_month.html"""
        people = [person_key.get() for person_key in month.people]
        money_usages = [money_usage.get() for money_usage in month.money_usages]

        person_key_to_name = {person.key: person.name for person in people}
        for item in month.items:
            item.buyer_name = person_key_to_name[item.buyer]

        buyers = [Buyer(person, money_usage) for person, money_usage in zip(people, money_usages)]

        self.render("month.html", errors=errors, format_number=format_number,
                    month=month, buyers=buyers, page_title=month.to_string_short())

    def add_item(self):
        """add an item to database"""
        # --------------- get info ----------------
        price = self.request.get("price")
        what = self.request.get("what")
        buyer = self.request.get("buyer")
        month = Month.get_current_month()

        # ---------------- validate ---------------
        errors = []
        # check if any month exist
        if month is None:
            errors.append("Please create a month before adding items")
        # check for empty fields
        if None in [price, what, buyer]:
            errors.append("Please fill all information")
        # check if buyer exists
        try:
            buyer = Key(urlsafe=buyer)
            if buyer not in month.people:
                raise ValueError
        except Exception:
            errors.append("Invalid buyer")
        # evaluate price
        try:
            if not re.match("^[0-9 \-+*/()]+$", price):
                raise SyntaxError
            price = eval(price)
            if price <= 0 or not isinstance(price, int):
                raise ValueError
        except (SyntaxError, ZeroDivisionError):
            errors.append("Invalid arithmetic expression in field price")
        except ValueError:
            errors.append("Price must be a positive integer")

        if len(errors) > 0:
            self.render_month(month, errors)
            return

        # ------------- put to database ----------------
        item = Item(
            buyer=buyer,
            price=price,
            what=what
        )
        month.items.append(item)
        month.update()
        ndb.sleep(0.5)

        self.render_month(month)


class Buyer(object):
    def __init__(self, person, money_usage):
        self.name = person.name
        self.key = person.key.urlsafe()
        self.spend = money_usage.money_spend
        self.last_month_left = self.round_float(money_usage.last_month_left)
        self.to_pay = self.round_float(money_usage.money_to_pay)
        self.round_up = money_usage.money_round_up
        self.next_month_left = self.round_float(money_usage.next_month_left)

    @staticmethod
    def round_float(f):
        return "{0:.2f}".format(f)


def format_number(n):
    if isinstance(n, float):
        return "{0:,.2f}".format(n).replace(',', ' ').split(".")
    else:
        return "{:,}".format(n).replace(',', ' ').split(".")


BaseHandler.jinja_env.globals['format_number'] = format_number
