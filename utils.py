from collections import deque
from functools import reduce
import requests, sys
from pymongo import MongoClient
import datetime


# opens a connection to the host and returns a new db
def mongo_connect(host):
    client = MongoClient(host)
    return client["moving-average"]


# create bid and ask deque pair
def create_deques(size):
    bid = deque(maxlen=size)
    ask = deque(maxlen=size)
    return bid, ask


# send request to the remote URL to fetch the latest data
# returns data (data from the request) and http status
def get_data(url):
    r = requests.get(url)
    if r.status_code != 200:
        return r.status_code
    return r.json()


# add new bid/ask averages to the beginning of the deques
def add_new_ba_avg(dq, bidask):
    dq.append(bidask)
    return dq


# reduce each deques to get the moving one minute average
def get_moving_average(dq):
    f = lambda a, b: a + b
    v = reduce(f, dq)/dq.maxlen
    return "{0:.8f}".format(v)


# persist the new one minute moving average
def persist(db, exch, currency_pair, bidavg, askavg):
    exch_col = db[exch]
    dt = datetime.datetime.utcnow()
    dp = {"pair": currency_pair, "time": dt, "bid": bidavg, "ask": askavg}
    return exch_col.insert_one(dp)


# print in-place (no scrolling)
def prip(text):
    sys.stdout.write("\r\x1b[K"+text.__str__())
    sys.stdout.flush()
