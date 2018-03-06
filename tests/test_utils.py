import utils
import pytest

# test deques
def test_create_deques():
    size = 20
    a, b = utils.create_deques(size)

    assert len(a) == 0
    assert len(b) == 0


def test_add_new_ba_average_moving_average():
    data1 = [1,2,3,4,5,6,7,8,9,10]

    a, b = utils.create_deques(len(data1))

    for n in data1:
        utils.add_new_ba_avg(a, n)
        utils.add_new_ba_avg(b, n)

    assert len(a) == 10
    assert len(b) == 10

    ma_a = utils.get_moving_average(a)
    assert float(ma_a) == 5.5

    ma_b = utils.get_moving_average(b)
    assert float(ma_b) == 5.5


def test_get_url_good():
    pair = "BTC_ETH"
    url = "https://poloniex.com/public?command=returnOrderBook&currencyPair=" + pair
    data = utils.get_data(url)
    assert "asks" in data
    assert "bids" in data

def test_get_url_bad_url():
    url = "https://www.cnet.com/fadsfaf/"
    data = utils.get_data(url)
    assert data == 404

def test_get_url_bad_pair():
    pair = "BTXC_XETH"
    url = "https://poloniex.com/public?command=returnOrderBook&currencyPair=" + pair
    data = utils.get_data(url)
    assert "error" in data
    assert data["error"] == "Invalid currency pair."
