import string

from google.appengine.ext import ndb

from config import app_config

NAME_MAX_LEN = app_config["person-name-max-length"]
INVALID_CHARS = set(string.punctuation.replace("_", ""))


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

    @classmethod
    def validate_name(cls, name):
        # check length
        if not 0 < len(name) <= NAME_MAX_LEN:
            return False
        # check uniqueness
        if not all(name != person.name for person in cls.get_all()):
            return False
        # check for invalid chars
        if len(set(name).intersection(INVALID_CHARS)) > 0:
            return False
        return True
