from datetime import datetime

from google.appengine.ext import ndb

from Item import Item
from MoneyUsage import MoneyUsage


def compute_number_of_people(month):
    return len(month.people)


class Month(ndb.Model):
    time_begin = ndb.DateTimeProperty(auto_now_add=True)
    time_end = ndb.DateTimeProperty()

    next_month = ndb.KeyProperty(kind="Month")
    prev_month = ndb.KeyProperty(kind="Month")

    people = ndb.KeyProperty(kind="Person", repeated=True)
    number_of_people = ndb.ComputedProperty(compute_number_of_people)
    money_usages = ndb.KeyProperty(kind="MoneyUsage", repeated=True)

    spend = ndb.IntegerProperty(default=0L)
    average = ndb.FloatProperty(default=0.0)

    items = ndb.StructuredProperty(Item, repeated=True)

    def to_string_short(self):
        return self.time_begin.strftime("%B %Y")

    def to_string_long(self):
        return self.time_begin.strftime("%d/%m/%y") + " - " + \
               (self.time_end.strftime("%d/%m/%y") if self.time_end is not None else "now")

    @classmethod
    def get_all(cls):
        return cls.query().order(-cls.time_begin).fetch()

    @classmethod
    def get_current_month(cls):
        m = cls.query().order(-cls.time_begin).fetch(1)
        return m[0] if len(m) > 0 else None

    @classmethod
    def end_month(cls):
        month = cls.get_current_month()
        if month and not month.time_end:
            month.time_end = datetime.now()
            month.put()
        return month

    @classmethod
    def new_month(cls, people_key_strings):
        people_keys = [ndb.Key(urlsafe=url_string) for url_string in people_key_strings]
        people = ndb.get_multi(people_keys)

        # get last month
        prev_month = cls.end_month()

        # new month
        new_month = Month(
            prev_month=prev_month.key,
            next_month=None,
            people=people_keys,
            money_usages=[],
            items=[]
        )
        new_month.put()

        # end prev month
        if prev_month:
            prev_month.next_month = new_month.key
            prev_month.put()

        # create money usages
        money_usages = []
        for person_key, person in zip(people_keys, people):
            money_usage = MoneyUsage(
                person=person_key,
                last_month_left=person.get_last_month_left(),
                month=new_month.key
            )
            money_usages.append(money_usage)
        ndb.put_multi(money_usages)
        money_usages = [money_usage.key for money_usage in money_usages]
        new_month.money_usages = money_usages

        # update last money usage of people
        for person, money_usage in zip(people, money_usages):
            person.last_money_usage = money_usage
        ndb.put_multi(people)

        # put new month, return
        new_month.put()
        ndb.sleep(0.7)
        return new_month

    def update(self, chain=False):
        self.spend = sum(item.price for item in self.items)
        self.average = self.spend * 1.0 / self.number_of_people

        for money_usage in ndb.get_multi(self.money_usages):
            money_usage.update(self, chain=chain)
            money_usage.put()

        self.put()

    def update_chain(self):
        month = self
        while month is not None:
            month.update(chain=True)
            month = month.next_month.get()

    @classmethod
    def update_all(cls):
        months = cls.get_all()
        if len(months) > 0:
            months[-1].update_chain()
