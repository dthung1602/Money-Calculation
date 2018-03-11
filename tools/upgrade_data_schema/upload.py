#!/usr/bin/env python -u

import os
import pickle
import sys
import traceback
from datetime import datetime
from httplib import HTTPSConnection
from urllib import quote_plus as percent_encode

try:
    import dev_appserver

    dev_appserver.fix_sys_path()
except ImportError:
    print('Please make sure the App Engine SDK is in your PYTHONPATH.')
    raise

from google.appengine.ext.remote_api import remote_api_stub
from google.appengine.ext import ndb
from models import *

app_id = os.environ['APP_ID']


def main():
    try:
        remote_api_stub.ConfigureRemoteApiForOAuth(
            '{}.appspot.com'.format(app_id),
            '/_ah/remote_api')
        convert(os.environ['PICKLE_FILE'])

    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stderr)
        exit(1)


def send_request(path, param_dict):
    # convert single value to one-element list
    for k in param_dict:
        v = param_dict[k]
        if isinstance(v, basestring):
            param_dict[k] = [v]

    # create content
    content = ""
    for k in param_dict:
        for v in param_dict[k]:
            if isinstance(v, unicode):  # encode unicode to utf8
                v = v.encode("utf-8")
            content += k + "=" + percent_encode(v) + "&"
    content = content[0:-1]  # remove trailing &

    # headers
    host_name = app_id + ".appspot.com"
    headers = {
        "Host": host_name,
        "Accept": "text/html",
        "Content-Type": "application/x-www-form-urlencoded",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": " 1",
    }

    # send
    connection = HTTPSConnection(host_name)
    connection.request("POST", path, content, headers)

    # return response status
    return connection.getresponse().status


def convert(file_name):
    # open file
    try:
        print "Opening file"
        f = open(file_name, "rb")

        # unpickle
        try:
            print "Unpickling"
            buyers = pickle.load(f)
            months = pickle.load(f)
            goods = pickle.load(f)
            # money_usages = pickle.load(f)

        except pickle.PickleError:
            print "ERROR occurred when unpickling"
            raise

    except IOError:
        print "Error opening file"
        raise
    finally:
        f.close()

    print "Start converting"

    # add all people
    print "Creating {} people".format(len(buyers))
    people = [Person(name=buyer.name) for buyer in buyers]
    ndb.put_multi(people)  # must be put so that they have keys

    # utilities for later parts
    buyer_id = [buyer.id for buyer in buyers]  # old id
    person_key_urlsafe = [person.key.urlsafe() for person in people]  # new key
    person_id_to_key_urlsafe = dict(zip(buyer_id, person_key_urlsafe))  # translate old id to new key

    # add month by month, from old to new
    print "Start creating months"
    for month in months:
        print "Month: " + datetime.ctime(month.time_begin)

        # create new month
        param = {
            "action": "new",
            "people": person_key_urlsafe  # add everyone to this month
        }
        status = send_request("/newmonth", param)

        # check if month is created
        if status != 302:
            raise Exception("Cannot create new month")

        current_month_key = Month.get_current_month_key()

        # get goods in this month
        goods_in_month = filter(lambda x: x.month_id == month.id, goods)

        # add items to month
        print "Adding {} items to this month".format(len(goods_in_month))
        for good in goods_in_month:
            # new item
            param = {
                "action": "add",
                "price": str(good.price),
                "what": good.what,
                "buyer": person_id_to_key_urlsafe[good.buyer]
            }
            status = send_request("/month/" + current_month_key.urlsafe(), param)

            # check if item is added
            if status != 200:
                raise Exception("Cannot add item")

            print "+",

        # change datetime of month
        print "\nChanging dates of month"
        current_month = current_month_key.get()
        current_month.time_begin = month.time_begin
        current_month.time_end = month.time_end

        # change datetime of items in month
        print "Changing dates of items"
        for item, good in zip(current_month.items, goods_in_month):
            item.date = good.date
            print "+",

        # update month
        current_month.put()
        ndb.sleep(0.5)
        print "\nFinished month"


if __name__ == '__main__':
    main()
