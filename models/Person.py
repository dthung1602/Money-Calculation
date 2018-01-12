from google.appengine.ext import ndb


class Person(ndb.Model):
    name = ndb.StringProperty(required=True)

    @classmethod
    def get_all(cls):
        return cls.query().fetch()
