from utils import mongo_connect, create_deques, add_new_ba_avg, get_moving_average, get_data, persist, prip
from multiprocessing import Process
from threading import Thread
import config, time, handlers, sys


def moving_average(db, cur1, cur2, exch, url, handler_name):
    max_deque_size = int(config.MOVING_AVERAGE_SIZE / config.POLL_RATE)
    bidq, askq = create_deques(max_deque_size)
    sample_count = 0

    while(True):

        handler = getattr(handlers, handler_name)
        ask_avg, bid_avg = handler(url, cur1, cur2)

        # look for an error (ask_avg == None, bid_avg has error message)
        if not ask_avg:
            print("error: ".format(bid_avg))
            return

        bidq = add_new_ba_avg(bidq, bid_avg)
        askq = add_new_ba_avg(askq, ask_avg)

        b_ma = get_moving_average(bidq)
        a_ma = get_moving_average(askq)

        sample_count += 1
        pair = "{}_{}".format(cur1, cur2)
        if sample_count >= max_deque_size:
            print("pair: {} exch: {} bid_avg: {} ask_avg: {}".format(pair, exch, b_ma, a_ma ))
        else:
            prip("need {} data samples to compute moving average".format(max_deque_size - sample_count))

        persist(db, exch, pair, b_ma, a_ma)
        time.sleep(config.POLL_RATE)


if __name__ == '__main__':

    if not len(sys.argv) > 2:
        print("enter a pair of cryptocurrencies separated by a space, e.g. 'BTC ETH'")
        exit(1)

    # get the currency pair from the command line
    cur1 = sys.argv[1]
    cur2 = sys.argv[2]

    # create a connection to mongo to persist time series data
    db = mongo_connect(config.MONGO_HOST)
    jobs = []
    # for each exchange, create
    for ex in config.exchanges:
        exname = ex["name"]
        exhandler = ex["handler"]
        # if bypass is set to 1 or true, bypass this exchange
        if ex["bypass"]:
            continue
        url = ex["url"]

        p = Thread(target=moving_average, args=(db, cur1, cur2, exname, url, exhandler))
        p.daemon = True
        jobs.append(p)
        p.start()

    for proc in jobs:
        proc.join()

