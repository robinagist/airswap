from functools import reduce
from utils import get_data


# handlers for exchange to get the bid and ask average for this data
# Poloniex
# def polx_handler(data):
def polx_handler(url, curr1, curr2):

    url_s = url + curr1 + "_" + curr2
    data = get_data(url_s)

    if not data:
        return None, "invalid URL: {}".format(url)
    if isinstance(data, int):
        return None, "error: HTTP status returned: {}".format(data)
    if "error" in data:
        return None, "service error: {}".format(data["error"])
    if "asks" and "bids" not in data:
        return None, "malformed data - no bids or asks"

    asks = [float(x[0]) for x in data["asks"]]
    bids = [float(x[0]) for x in data["bids"]]

    f = lambda a,b: a + b
    ask_avg = reduce(f, asks)/len(asks)
    bid_avg = reduce(f, bids)/len(bids)
    return ask_avg, bid_avg

# GDAX
def gdax_handler(url, curr1, curr2):
    url_s = url.format(curr2, curr1)
    data = get_data(url_s)

    if not data:
        return None, "invalid URL: {}".format(url)
    if isinstance(data, int):
        return None, "error: HTTP status returned: {}".format(data)
    if "error" in data:
        return None, "service error: {}".format(data["error"])
    if "asks" and "bids" not in data:
        return None, "malformed data - no bids or asks"

    asks = [float(x[0]) for x in data["asks"]]
    bids = [float(x[0]) for x in data["bids"]]

    f = lambda a,b: a + b
    ask_avg = reduce(f, asks)/len(asks)
    bid_avg = reduce(f, bids)/len(bids)
    return ask_avg, bid_avg