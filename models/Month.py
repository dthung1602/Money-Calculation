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
        return "{} ({} - {})".format(self.to_string_short(), self.time_begin_format(), self.time_end_format())

    def time_begin_format(self):
        return self.time_begin.strftime("%d/%m/%y")

    def time_end_format(self):
        return self.time_end.strftime("%d/%m/%y") if self.time_end else "now"

    @classmethod
    def get_all(cls):
        return cls.query().order(-cls.time_begin).fetch()

    @classmethod
    def get_current_month(cls):
        m = cls.query().order(-cls.time_begin).fetch(1)
        return m[0] if len(m) > 0 else None

    @classmethod
    def get_current_month_key(cls):
        m = cls.query().order(-cls.time_begin).fetch(1, keys_only=True)
        return m[0] if len(m) > 0 else None

    @classmethod
    def end_month(cls):
        """
            End current month if it is not ended
            :return current month
        """
        month = cls.get_current_month()
        if month and not month.time_end:
            month.time_end = datetime.now()
            month.put()
        return month

    @classmethod
    def new_month(cls, people_key_strings):
        """
            End current month, create and return a new month
            :return new month
        """

        people_keys = [ndb.Key(urlsafe=url_string) for url_string in people_key_strings]
        people = ndb.get_multi(people_keys)

        # get last month
        prev_month = cls.end_month()

        # new month
        new_month = Month(
            prev_month=prev_month.key if prev_month else None,
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
            lml = person.get_last_month_left()
            money_usage = MoneyUsage(
                person=person_key,
                money_to_pay=-lml,
                last_month_left=lml,
                month=new_month.key
            )
            money_usages.append(money_usage)
        ndb.put_multi(money_usages)
        money_usages = [money_usage.key for money_usage in money_usages]
        new_month.money_usages = money_usages
        new_month.put()

        # update last money usage of people
        # and update next_money_usage
        for person, money_usage in zip(people, money_usages):
            if person.last_money_usage:
                lmu = person.last_money_usage.get()
                lmu.next_money_usage = money_usage
                lmu.put()
            person.last_money_usage = money_usage
        ndb.put_multi(people)

        ndb.sleep(0.7)
        return new_month

    def update(self):
        """Recalculate properties of month when items are modified/deleted"""

        self.spend = sum(item.price for item in self.items)
        self.average = self.spend * 1.0 / self.number_of_people
        self.put()

        money_usages = ndb.get_multi(self.money_usages)
        for mu in money_usages:
            mu.update(self)

        ndb.sleep(0.1)

    def update_chain(self):
        """Update this month and all following months"""

        months = Month.query().filter(Month.time_begin >= self.time_begin).fetch()
        for month in months:
            month.update()

    @classmethod
    def update_all(cls):
        """Update all months, start from first month"""

        first_month = cls.query().order(cls.time_begin).fetch(1)
        if first_month:
            first_month.update_chain()
