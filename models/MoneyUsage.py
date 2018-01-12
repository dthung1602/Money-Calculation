from math import ceil

from google.appengine.ext import ndb


def compute_next_month_left(money_usage):
    # calculate next month left
    value = money_usage.money_round_up - money_usage.money_to_pay

    # if next month exist, update next month
    next_month = money_usage.parent().next_month.get()
    if next_month:
        next_month.last_month_left = value

    return value


def compute_money_spend(money_usage):
    return sum(item.price for item in money_usage.parent().items if item.buyer == money_usage.person)


def compute_money_to_pay(money_usage):
    return money_usage.parent().average - money_usage.money_spend - money_usage.last_month_left


def compute_round_up(money_usage):
    return int(ceil(money_usage.money_to_pay / 10.0) * 10)


class MoneyUsage(ndb.Model):
    """
        Summarize spending of a buyer in a month
        Each instance needs to have a Month instance as parent
    """
    person = ndb.KeyProperty(required=True)

    last_month_left = ndb.FloatProperty(required=True)
    next_month_left = ndb.ComputedProperty(compute_next_month_left)

    money_spend = ndb.ComputedProperty(compute_money_spend)  # actual spending in month
    money_to_pay = ndb.ComputedProperty(compute_money_to_pay)  # money to pay, after subtracting last month left, ...
    money_round_up = ndb.ComputedProperty(compute_round_up)  # actual money to pay, round up for convenience
