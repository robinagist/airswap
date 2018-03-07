# Airswap
# Airswap technical assessment

03.07.2018

This is the code for the Airswap technical, as quoted from Richard:
```
1. Takes an argument for a pair of crypto currencies like ETH/BTC (Ethereum and Bitcoin) 
2. Connects to the Poloniex exchange (https://poloniex.com) 
3. Calculates a 1-minute simple moving average of price for the provided token pair on an ongoing basis 
4. Displays the value in the shell while the program is running

We are interested in the completeness of the exercise and your coding style. Based on your particular skill set, consider adding any of the following features (or expand on the core requirements with your own flair):

Stores state in a scalable manner
Handles additional third party data streams, including errors and unavailable data streams
Is coded entirely in a functional style where all variables are immutable
Contains 90% or more test coverage, including edge case tests
```

Features:
+ moving average generator - configured for 60 second MA, but can be configured for any moving average
+ configurable polling/sampling rate
+ works with both POLONIEX and GDAX  (though you might have trouble finding two currencies that match on both - try BTC ETH)
+ can be extended to other exchanges by simply adding a handler and a configuration entry
+ optionally persists moving average data to Mongo collections for each exchange and currency combo

# running it
NOTE: I use python 3.6 and run inside of virtualenv
```
0. REQUIRES: 
    requests  (pip install requests)
    pymongo (pip install pymongo)
    mongodb (local installation) 
    NOTE: to run without Mongo, set config.PERSIST to False
    
1. pull it from github 
2. go to the `airswap` directory
3. in config.py, change the mongodb URL to match your installation
(alternatively, set PERSIST to 'False' to not save the time series data)
4. run with `python3 main.py BTC ETH`
(takes one minute to load enough data, then scrolls average based on config.POLL_RATE)
5. to stop, just hit CTRL-C

NOTE:  to turn off polling data from an exchange, set 'bypass' to True in config.py
```
When using multiple data sources, it can error on one URL, and still keep functioning in other threads.

    

