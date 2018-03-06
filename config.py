import utils

# text colors
HEADER = '\033[95m'
SAME = '\033[94m'
UP = '\033[92m'
WARNING = '\033[93m'
DOWN = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

# exchanges
exchanges = [
    {
        "bypass":1,
        "name": "GDAX",
        "url": "https://",
        "handler": utils.gdax_handler
     },
    {
        "bypass":0,
        "name": "POLX",
        "url": "https://poloniex.com/public?command=returnOrderBook&currencyPair=",
        "handler": utils.polx_handler
    }]

MOVING_AVERAGE_SIZE = 60    # in seconds
POLL_RATE = 1               # in seconds

MONGO_HOST = "mongodb://localhost:27017/"