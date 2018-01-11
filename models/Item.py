class Good(db.Model):
    month_id = db.IntegerProperty(required=True)
    date = db.DateTimeProperty(auto_now_add=True)
    price = db.IntegerProperty(required=True)
    what = db.StringProperty(required=True)
    buyer = db.IntegerProperty(required=True)