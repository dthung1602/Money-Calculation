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
