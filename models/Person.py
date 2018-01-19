from google.appengine.ext import ndb

from config import app_config


class Person(ndb.Model):
    name = ndb.StringProperty(required=True)
    last_money_usage = ndb.KeyProperty(kind="MoneyUsage")

    NAME_MAX_LEN = app_config["person-name-max-length"]

    def get_last_month_left(self):
        if self.last_money_usage is None:
            return 0
        else:
            return self.last_money_usage.get().next_month_left

    @classmethod
    def get_all(cls):
        return cls.query().order(Person.name).fetch()

    @classmethod
    def validate_name(cls, name):
        return 0 < len(name) <= cls.NAME_MAX_LEN and all(name != person.name for person in cls.get_all())
