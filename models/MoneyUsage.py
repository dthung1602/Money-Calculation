from math import ceil

from google.appengine.ext import ndb


def compute_next_month_left(money_usage):
    return money_usage.money_round_up - money_usage.money_to_pay


def compute_round_up(money_usage):
    return int(ceil(money_usage.money_to_pay / 10.0) * 10)


class MoneyUsage(ndb.Model):
    """
        Summarize spending of a buyer in a month
        Each instance needs to have a Month instance as parent
    """

    person = ndb.KeyProperty(kind="Person", required=True)
    month = ndb.KeyProperty(kind="Month", required=True)

    last_month_left = ndb.FloatProperty(required=True)
    next_month_left = ndb.ComputedProperty(compute_next_month_left)

    next_money_usage = ndb.KeyProperty()

    money_spend = ndb.IntegerProperty(default=0, required=True)  # actual spending in month
    money_to_pay = ndb.FloatProperty(required=True)  # money to pay = month average - last month left - spend in month
    money_round_up = ndb.ComputedProperty(compute_round_up)  # actual money to pay, round up for convenience

    def update(self, month=None):
        """
            Recalculate properties of this money usage & following money usages
            :param month: month object which self belongs to
                          month might has changed without being put -> must be passed so that new info is used
                          if month is not passed, month will be loaded from db
        """

        if not month:
            month = self.month.get()

        # update info from month
        self.money_spend = sum(item.price for item in month.items if item.buyer == self.person)
        self.money_to_pay = month.average - self.money_spend - self.last_month_left

        # buffer -> avoid reload one month multiple time
        month_key_to_average = {}

        # update next money usages
        money_usages = [self]
        mu = self
        while mu.next_money_usage:
            # update last month left
            next_mu = mu.next_money_usage.get()
            next_mu.last_month_left = mu.next_month_left

            # get month average
            if next_mu.month in month_key_to_average:  # if month in buffer
                next_mu_month_average = month_key_to_average[next_mu.month]
            else:  # month not in buffer -> get average & save in buffer
                next_mu_month_average = next_mu.month.get().average
                month_key_to_average[next_mu.month] = next_mu_month_average

            # update money to pay
            next_mu.money_to_pay = next_mu_month_average - next_mu.money_spend - next_mu.last_month_left

            mu = next_mu
            money_usages.append(mu)

        ndb.put_multi(money_usages)
