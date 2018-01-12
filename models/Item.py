from google.appengine.ext import ndb


class Item(ndb.Model):
    date = ndb.DateTimeProperty(auto_now_add=True)
    buyer = ndb.KeyProperty(required=True)
    price = ndb.IntegerProperty(required=True)
    what = ndb.StringProperty(required=True)
