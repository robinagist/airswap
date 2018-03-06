from collections import deque
from functools import reduce
import requests
import config
from pymongo import MongoClient
import datetime


# opens a connection to the host and returns a new db
def mongo_connect(host):
    client = MongoClient(host)
    return client["moving-average"]


# create bid and ask deque pair
def create_deques():
    bid = deque()
    ask = deque()
    bid.maxlen = config.MOVING_AVERAGE_SIZE / config.POLL_RATE
    ask.maxlen = config.MOVING_AVERAGE_SIZE / config.POLL_RATE
    return bid, ask


# send request to the remote URL to fetch the latest data
# returns data (data from the request) and http status
def get_data(url):
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception("http error: {}".format(r.status_code))
    return r.json


# handler for exchange to get the bid and ask average for this data
def polx_handler(data):
    if "asks" or "bids" not in data:
        return None, None

    asks = [float(x[0]) for x in data["asks"]]
    bids = [float(x[0]) for x in data["bids"]]
    f = lambda a,b: a + b
    ask_avg = reduce(f, asks)/len(asks)
    bid_avg = reduce(f, bids)/len(bids)
    return ask_avg, bid_avg


def gdax_handler(data):
    pass


# add new bid/ask averages to the beginning of the deques
def add_new_ba_avg(dq: deque, bidask: float):
    dq.append(bidask)
    return dq


# reduce each deques to get the moving one minute average
def get_moving_average(dq: deque):
    f = lambda a, b: a + b
    return reduce(f, dq)/dq.maxlen


# persist the new one minute moving average
def persist(db, exch, currency_pair, bidavg, askavg):
    exch_col = db[exch]
    dt = datetime.datetime.utcnow()
    dp = {"pair": currency_pair, "time": dt, "bid": bidavg, "ask": askavg}
    return exch_col.insert_one(dp)

