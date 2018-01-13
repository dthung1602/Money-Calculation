from google.appengine.ext import ndb


class Person(ndb.Model):
    name = ndb.StringProperty(required=True)
    last_money_usage = ndb.KeyProperty(kind="MoneyUsage")

    def get_last_month_left(self):
        if self.last_money_usage is None:
            return 0
        else:
            return self.last_money_usage.get().next_month_left

    @classmethod
    def get_all(cls):
        return cls.query().order(Person.name).fetch()
