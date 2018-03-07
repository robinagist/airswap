# configuration

# exchanges
exchanges = [
    {
        "bypass": 0,
        "name": "GDAX",
        "url": "https://api.gdax.com/products/{}-{}/book?level=2",
        "handler": "gdax_handler"
     },
    {
        "bypass": 0,
        "name": "POLX",
        "url": "https://poloniex.com/public?command=returnOrderBook&currencyPair=",
        "handler": "polx_handler"
    }]

MOVING_AVERAGE_SIZE = 60    # in seconds
POLL_RATE = 1               # in seconds
PERSIST = False
MONGO_HOST = "mongodb://localhost:27017/"