class MoneyUsage(db.Model):
    buyer_id = db.IntegerProperty(required=True)
    month_id = db.IntegerProperty(required=True)

    last_month_left = db.FloatProperty(required=True)
    next_month_left = db.FloatProperty(required=True)

    money_spend = db.IntegerProperty(required=True)
    money_to_pay = db.FloatProperty(required=True)
    roundup = db.IntegerProperty(required=True)

    @staticmethod
    def get_usage_in_month(month):
        return db.GqlQuery("SELECT * FROM MoneyUsage WHERE month_id={}".format(month.key().id()))

    @staticmethod
    def update(good):
        avg_price = good.price * 1.0 / Buyer.get_number_of_buyers()
        for usage in db.GqlQuery("SELECT * FROM MoneyUsage WHERE month_id={}".format(good.month_id)):
            usage.money_to_pay += avg_price
            if usage.buyer_id == good.buyer:
                usage.money_spend += good.price
                usage.money_to_pay -= good.price
            usage.roundup = round_up10(usage.money_to_pay)
            usage.next_month_left = usage.roundup - usage.money_to_pay
            usage.put()
        sleep(0.8)
