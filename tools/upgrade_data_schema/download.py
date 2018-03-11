#!/usr/bin/env python -u

import os
import pickle
import sys
import traceback


try:
    import dev_appserver

    dev_appserver.fix_sys_path()
except ImportError:
    print('Please make sure the App Engine SDK is in your PYTHONPATH.')
    raise

from google.appengine.ext.remote_api import remote_api_stub
from oldmodels import *
from tempmodels import *


def main():
    try:
        app_id = os.environ['APP_ID']
        remote_api_stub.ConfigureRemoteApiForOAuth(
            '{}.appspot.com'.format(app_id),
            '/_ah/remote_api')

        download(os.environ['PICKLE_FILE'])
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stderr)
        exit(1)


def download(file_name):
    # open file
    try:
        print "Opening file"
        f = open(file_name, "wb")

        try:
            # pickle buyers
            print "Downloading buyers"
            buyers = Buyer.get_all_buyers()
            print "Pickling"
            buyers = [TempBuyer(buyer) for buyer in buyers]
            pickle.dump(buyers, f)

            # pickle months
            print "Downloading months"
            months = db.GqlQuery("SELECT * FROM Month ORDER BY time_begin ASC")
            print "Pickling"
            months = [TempMonth(month) for month in months]
            pickle.dump(months, f)

            # pickle goods
            print "Downloading goods"
            goods = db.GqlQuery("SELECT * FROM Good ORDER BY date ASC")
            print "Pickling"
            goods = [TempGood(good) for good in goods]
            pickle.dump(goods, f)

            # pickle money usages
            # print "Downloading money usages"
            # money_usages = db.GqlQuery("SELECT * FROM MoneyUsage ORDER BY month_id ASC")
            # print "Pickling"
            # money_usages = [TempMoneyUsage(money_usage) for money_usage in money_usages]
            # pickle.dump(money_usages, f)

        except pickle.PickleError:
            print "ERROR occurred"
            raise

    except IOError:
        print "Error opening file"
        raise
    finally:
        f.close()

    print "Complete downloading!"


if __name__ == '__main__':
    main()
