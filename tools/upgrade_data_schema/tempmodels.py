class TempBuyer:
    def __init__(self, entity):
        self.id = entity.key().id()
        self.name = entity.name


class TempMonth:
    def __init__(self, entity):
        self.id = entity.key().id()
        self.spend = entity.spend
        self.average = entity.average
        self.time_begin = entity.time_begin
        self.time_end = entity.time_end
        self.next_month = entity.next_month
        self.prev_month = entity.prev_month


class TempGood:
    def __init__(self, entity):
        self.id = entity.key().id()
        self.month_id = entity.month_id
        self.date = entity.date
        self.price = entity.price
        self.what = entity.what
        self.buyer = entity.buyer


class TempMoneyUsage:
    def __init__(self, entity):
        self.id = entity.key().id()
        self.buyer_id = entity.buyer_id
        self.month_id = entity.month_id
        self.last_month_left = entity.last_month_left
        self.next_month_left = entity.next_month_left
        self.money_spend = entity.money_spend
        self.money_to_pay = entity.money_to_pay
        self.roundup = entity.roundup
