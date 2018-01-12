from google.appengine.ext import ndb

import Item
import MoneyUsage


def compute_spend(month):
    return sum(item.price for item in month.items)


def compute_average(month):
    last_month_left = sum(money_usage.last_month_left for money_usage in month.money_usages)
    return (month.spend - last_month_left) / month.number_of_people


def compute_number_of_people(month):
    return len(month.people)


class Month(ndb.Model):
    time_begin = ndb.DateTimeProperty(auto_now_add=True)
    time_end = ndb.DateTimeProperty()

    next_month = ndb.KeyProperty(kind="Month")
    prev_month = ndb.KeyProperty(kind="Month")

    people = ndb.KeyProperty(kind="Buyer", repeated=True)
    number_of_people = ndb.ComputedProperty(compute_number_of_people)
    money_usages = ndb.StructuredProperty(MoneyUsage, repeated=True)
    # money_usage = ndb.KeyProperty(kind="MoneyUsage", repeated=True)

    spend = ndb.ComputedProperty(compute_spend)
    average = ndb.ComputedProperty(compute_average)

    items = ndb.StructuredProperty(Item, repeated=True)

    def to_string_short(self):
        return self.time_begin.strftime("%B %Y")

    def to_string_long(self):
        return self.time_begin.strftime("%d/%m/%y") + " - " + \
               (self.time_end.strftime("%d/%m/%y") if self.time_end is not None else "now")
