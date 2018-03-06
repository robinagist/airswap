# configuration

# exchanges
exchanges = [
    {
        "bypass":1,
        "name": "GDAX",
        "url": "https://",
        "handler": "gdax_handler"
     },
    {
        "bypass":0,
        "name": "POLX",
        "url": "https://poloniex.com/public?command=returnOrderBook&currencyPair=",
        "handler": "polx_handler"
    }]

MOVING_AVERAGE_SIZE = 60    # in seconds
POLL_RATE = 1               # in seconds

MONGO_HOST = "mongodb://localhost:27017/"