from math import ceil

from google.appengine.ext import ndb


def compute_next_month_left(money_usage):
    return money_usage.money_round_up - money_usage.money_to_pay


def compute_round_up(money_usage):
    return int(ceil(money_usage.money_to_pay / 10.0) * 10)


class MoneyUsage(ndb.Model):
    """
        Summarize spending of a buyer in a month
        Each instance needs to have a Month instance as parent
    """

    person = ndb.KeyProperty(kind="Person", required=True)
    month = ndb.KeyProperty(kind="Month", required=True)

    last_month_left = ndb.FloatProperty(required=True)
    next_month_left = ndb.ComputedProperty(compute_next_month_left)

    money_spend = ndb.IntegerProperty(default=0, required=True)  # actual spending in month
    money_to_pay = ndb.FloatProperty(default=0.0, required=True)  # money to pay, after subtracting last month left, ...
    money_round_up = ndb.ComputedProperty(compute_round_up)  # actual money to pay, round up for convenience

    def update(self, month, chain=False):
        self.money_spend = sum(item.price for item in month.items if item.buyer == self.person)
        self.money_to_pay = month.average - self.money_spend - self.last_month_left
        self.put()

        # TODO
        if chain:
            pass
