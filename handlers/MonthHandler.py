from google.appengine.ext.ndb import Key

from BaseHandler import Handler
from models import Month, MoneyUsage, Person


class MonthHandler(Handler):
    """Handle request for a particular month"""

    def get(self, month_key):
        """Get month info and render html"""
        try:
            month = Key(urlsafe=month_key)
            if month is None:
                raise Exception
        except:
            self.render("4xx.html", code=404, error_name="Not found")
        else:
            self.render_month(month.get())

    def post(self, month_key):
        """Handle adding new item"""
        self.add_item()
        self.redirect("/month/" + month_key)

    def render_month(self, month, error=None):
        """Render money_current_month.html"""
        people = [person_key.get() for person_key in month.people]
        money_usages = [money_usage.get() for money_usage in month.money_usages]

        person_key_to_name = {person.key: person.name for person in people}
        for item in month.items:
            item.buyer_name = person_key_to_name[item.buyer]

        buyers = [Buyer(person, money_usage) for person, money_usage in zip(people, money_usages)]

        self.render("month.html", error=error, format_float=format_float,
                    month=month, buyers=buyers, page_title=month.to_string_short())

    def add_item(self):
        pass
        # """add a good to database"""
        # # get info
        # price = self.request.get("price")
        # what = self.request.get("what")
        # buyer = self.request.get("buyer")
        #
        # # validate
        # error = []
        # # check for empty fields
        # if None in [price, what, buyer]:
        #     error.append("Please fill all information")
        # # check if buyer exists
        # try:
        #     buyer = int(buyer)
        #     if Person.get_by_id(buyer) is None:
        #         raise ValueError
        # except ValueError:
        #     error.append("Invalid buyer")
        # # evaluate price
        # try:
        #     if not re.match("^[0-9 \-+*/()]+$", price):
        #         raise SyntaxError
        #     price = eval(price)
        #     if price <= 0 or not isinstance(price, int):
        #         raise ValueError
        # except (SyntaxError, ZeroDivisionError):
        #     error.append("Invalid arithmetic expression in field price")
        # except ValueError:
        #     error.append("Price must be a positive integer")
        #
        # if len(error) > 0:
        #     self.render_month(month, error)
        #     return
        #
        # # put to database
        # good = Good(month_id=month_id, price=price, what=what, buyer=buyer)
        # good.put()
        # sleep(0.5)
        # MoneyUsage.update(good)
        # month.update()
        # self.render_month(month)

    def end_month(self, old_month):
        pass
        # """
        #     add time_end to old month, making its data can not be change;
        #     create a new month
        # """
        # # check if old_month has already ended
        # if old_month.time_end is not None:
        #     self.render_month(old_month, ["This month has already ended."])
        #     return
        #
        # # create new month
        # new_month = Month.new_month(old_month)
        #
        # # end old month
        # old_month.time_end = datetime.now()
        # old_month.next_month = new_month.key().id()
        # old_month.put()
        #
        # sleep(0.8)
        # self.render_month(old_month)


class Buyer(object):
    def __init__(self, person, money_usage):
        self.name = person.name
        self.spend = self.round_float(money_usage.money_spend)
        self.last_month_left = self.round_float(money_usage.last_month_left)
        self.to_pay = self.round_float(money_usage.money_to_pay)
        self.round_up = money_usage.money_round_up
        self.next_month_left = self.round_float(money_usage.next_month_left)

    @staticmethod
    def round_float(f):
        return "{0:.2f}".format(f)


def format_float(n):
    if isinstance(n, float):
        print("int")
        return "{0:,.2f}".format(n).replace(',', ' ').split(".")
    else:
        print("float")
        return "{:,}".format(n).replace(',', ' ').split(".")
