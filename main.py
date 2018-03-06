import sys
from utils import mongo_connect, create_deques, add_new_ba_avg, get_moving_average, get_data, persist
import config
from multiprocessing import Process
import time



def moving_average(db, pair, exch, url, handler):

    bidq, askq = create_deques()
    while(True):
        data = get_data(url)
        ask_avg, bid_avg = handler(data)

        bidq = add_new_ba_avg(bidq, bid_avg)
        askq = add_new_ba_avg(askq, ask_avg)

        b_ma = get_moving_average(bidq)
        a_ma = get_moving_average(askq)

        # TODO output to screen
        persist(db, exch, pair, b_ma, a_ma)

        time.sleep(config.POLL_RATE)


# get the currency pair from the command line
cur1 = sys.argv[1]
cur2 = sys.argv[2]
cstr = "{}_{}".format(cur1, cur2)

# create a connection to mongo to persist time series data
db = mongo_connect(config.MONGO_HOST)

# for each exchange, create
for ex in config.exchanges:
    # if config is set to 1 or true, bypass this exchange
    if ex["bypass"]:
        continue
    url = ex["url"] + cstr
    p = Process(target=moving_average(db, cstr, ex["name"], url, ex["handler"]))
    p.start()

    p.join()
