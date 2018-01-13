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
        return cls.query().order(-cls.time_begin).fetch(5)

    @classmethod
    def new_month(cls, request):
        # get & validate info in request
        url_strings = request.get_all("people")
        if len(url_strings) == 0:
            raise ValueError("There must be at least one person in a month.")
        people_keys = [ndb.Key(urlsafe=url_string) for url_string in url_strings]
        people = [pk.get() for pk in people_keys]

        # get last month
        months = cls.get_all()
        prev_month = months[0].key if len(months) > 0 else None

        # new month
        new_month = Month(
            prev_month=prev_month,
            next_month=None,
            people=people_keys,
            money_usages=[],
            items=[]
        )
        new_month.put()

        # create money usages
        money_usages = []
        for person_key, person in zip(people_keys, people):
            # new money usage
            money_usage = MoneyUsage(
                person=person_key,
                last_month_left=person.get_last_month_left(),
                month=new_month.key
            )
            # put and add
            money_usage.put()
            money_usages.append(money_usage.key)

        new_month.money_usages = money_usages

        # update last money usage of people
        for person, money_usage in zip(people, money_usages):
            person.last_money_usage = money_usage
            person.put()

        # put new month, return
        new_month.put()
        ndb.sleep(0.7)
        return new_month

    def update(self, chain=False):
        last_month_left = sum(money_usage.get().last_month_left for money_usage in self.money_usages)
        self.spend = sum(item.price for item in self.items)
        self.average = (self.spend - last_month_left) / self.number_of_people

        for money_usage in self.money_usages:
            money_usage.update(self, chain=chain)

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
