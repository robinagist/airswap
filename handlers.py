from functools import reduce


# handlers for exchange to get the bid and ask average for this data
# Poloniex
def polx_handler(data):
    if "asks" and "bids" not in data:
        return None, None

    asks = [float(x[0]) for x in data["asks"]]
    bids = [float(x[0]) for x in data["bids"]]
    f = lambda a,b: a + b
    ask_avg = reduce(f, asks)/len(asks)
    bid_avg = reduce(f, bids)/len(bids)
    return ask_avg, bid_avg

# GDAX
def gdax_handler(data):
    pass