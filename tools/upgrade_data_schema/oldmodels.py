from datetime import timedelta
from math import ceil
from time import sleep

from google.appengine.ext import db


def round_up10(n):
    return int(ceil(n / 10.0) * 10)


class Buyer(db.Model):
    name = db.StringProperty(required=True)

    __number_of_buyers__ = None

    @staticmethod
    def get_all_buyers():
        return db.GqlQuery("SELECT * FROM Buyer ORDER BY name ASC")

    @classmethod
    def get_number_of_buyers(cls):
        if not cls.__number_of_buyers__:
            cls.__number_of_buyers__ = cls.all(keys_only=True).count()
        return cls.__number_of_buyers__

    def get_money_in_month(self, month):
        goods = db.GqlQuery(
            "SELECT * FROM Good WHERE month_id={} AND buyer={} ORDER BY date ASC".format(month.key().id(),
                                                                                         self.key().id()))
        return sum(good.price for good in goods)


class Month(db.Model):
    spend = db.IntegerProperty()
    average = db.FloatProperty()

    time_begin = db.DateTimeProperty(auto_now_add=True)
    time_end = db.DateTimeProperty()

    next_month = db.IntegerProperty()
    prev_month = db.IntegerProperty()

    @staticmethod
    def new_month(old_month=None):
        # create new month
        month = Month(spend=0, average=0.0)
        buyers = list(Buyer.get_all_buyers())

        # link new month to old month
        old_month_money_usages = {}
        if old_month is not None:
            month.prev_month = old_month.key().id()
            usages = MoneyUsage.get_usage_in_month(old_month)
            old_month_money_usages = {usage.buyer_id: usage.next_month_left for usage in usages}

        month.put()
        sleep(0.3)

        # create corresponding money usage for each user in this month
        for buyer in buyers:
            bid = buyer.key().id()
            last_month_left = old_month_money_usages.get(bid, 0.0)
            money_usage = MoneyUsage(
                buyer_id=bid,
                month_id=month.key().id(),
                last_month_left=last_month_left,
                next_month_left=last_month_left,
                money_spend=0,
                money_to_pay=-last_month_left,
                roundup=0
            )
            money_usage.put()

        sleep(1)
        return month

    def update(self):
        nob = Buyer.get_number_of_buyers()
        self.spend = self.sum()
        self.average = (self.spend * 1.0 / nob) if nob > 0 else 0.0
        self.put()
        sleep(0.5)

    def to_string_short(self):
        new_time = self.time_begin + timedelta(days=4)
        if new_time.month != self.time_begin.month:
            return new_time.month.strftime("%B %Y")
        return self.time_begin.strftime("%B %Y")

    def to_string_long(self):
        return self.time_begin.strftime("%d/%m/%y") + " - " + \
               (self.time_end.strftime("%d/%m/%y") if self.time_end is not None else "now")

    def get_goods(self):
        goods = []
        for good in db.GqlQuery("SELECT * FROM Good WHERE month_id={} ORDER BY date ASC".format(self.key().id())):
            good.buyer_name = Buyer.get_by_id(int(good.buyer)).name
            goods.append(good)
        return goods

    def sum(self):
        return sum(good.price for good in self.get_goods())


class Good(db.Model):
    month_id = db.IntegerProperty(required=True)
    date = db.DateTimeProperty(auto_now_add=True)
    price = db.IntegerProperty(required=True)
    what = db.StringProperty(required=True)
    buyer = db.IntegerProperty(required=True)


class MoneyUsage(db.Model):
    buyer_id = db.IntegerProperty(required=True)
    month_id = db.IntegerProperty(required=True)

    last_month_left = db.FloatProperty(required=True)
    next_month_left = db.FloatProperty(required=True)

    money_spend = db.IntegerProperty(required=True)
    money_to_pay = db.FloatProperty(required=True)
    roundup = db.IntegerProperty(required=True)

    @staticmethod
    def get_usage_in_month(month):
        return db.GqlQuery("SELECT * FROM MoneyUsage WHERE month_id={}".format(month.key().id()))

    @staticmethod
    def update(good):
        avg_price = good.price * 1.0 / Buyer.get_number_of_buyers()
        for usage in db.GqlQuery("SELECT * FROM MoneyUsage WHERE month_id={}".format(good.month_id)):
            usage.money_to_pay += avg_price
            if usage.buyer_id == good.buyer:
                usage.money_spend += good.price
                usage.money_to_pay -= good.price
            usage.roundup = round_up10(usage.money_to_pay)
            usage.next_month_left = usage.roundup - usage.money_to_pay
            usage.put()
        sleep(0.8)
