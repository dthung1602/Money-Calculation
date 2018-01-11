class Month(db.Model):
    spend = db.IntegerProperty()
    average = db.FloatProperty()

    time_begin = db.DateTimeProperty(auto_now_add=True)
    time_end = db.DateTimeProperty()

    next_month = db.IntegerProperty()
    prev_month = db.IntegerProperty()

    @staticmethod
    def new_month(old_month=None):
        # create new month
        month = Month(spend=0, average=0.0)
        buyers = list(Buyer.get_all_buyers())

        # link new month to old month
        old_month_money_usages = {}
        if old_month is not None:
            month.prev_month = old_month.key().id()
            usages = MoneyUsage.get_usage_in_month(old_month)
            old_month_money_usages = {usage.buyer_id: usage.next_month_left for usage in usages}

        month.put()
        sleep(0.3)

        # create corresponding money usage for each user in this month
        for buyer in buyers:
            bid = buyer.key().id()
            last_month_left = old_month_money_usages.get(bid, 0.0)
            money_usage = MoneyUsage(
                buyer_id=bid,
                month_id=month.key().id(),
                last_month_left=last_month_left,
                next_month_left=last_month_left,
                money_spend=0,
                money_to_pay=-last_month_left,
                roundup=0
            )
            money_usage.put()

        sleep(1)
        return month

    def update(self):
        nob = Buyer.get_number_of_buyers()
        self.spend = self.sum()
        self.average = (self.spend * 1.0 / nob) if nob > 0 else 0.0
        self.put()
        sleep(0.5)

    def to_string_short(self):
        new_time = self.time_begin + timedelta(days=4)
        if new_time.month != self.time_begin.month:
            return new_time.month.strftime("%B %Y")
        return self.time_begin.strftime("%B %Y")

    def to_string_long(self):
        return self.time_begin.strftime("%d/%m/%y") + " - " + \
               (self.time_end.strftime("%d/%m/%y") if self.time_end is not None else "now")

    def get_goods(self):
        goods = []
        for good in db.GqlQuery("SELECT * FROM Good WHERE month_id={} ORDER BY date ASC".format(self.key().id())):
            good.buyer_name = Buyer.get_by_id(int(good.buyer)).name
            goods.append(good)
        return goods

    def sum(self):
        return sum(good.price for good in self.get_goods())
