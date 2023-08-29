################################################################################
#
#  Permission is hereby granted, free of charge, to any person obtaining a
#  copy of this software and associated documentation files (the "Software"),
#  to deal in the Software without restriction, including without limitation
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,
#  and/or sell copies of the Software, and to permit persons to whom the
#  Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
#  OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.

# Quoted ABC at (bid:115.46, ask:116.63, price:115.46)
# Quoted DEF at (bid:115.14, ask:116.05, price:115.14)
# Ratio 1

import json
import random
import urllib.request
from typing import Optional, TypedDict, Dict
from dataclasses import dataclass

# Server API URLs
QUERY = "http://localhost:8080/query?id={}"

# 500 server request
N = 500


class Quote(TypedDict):
    """A quote object."""

    id: str
    stock: str
    timestamp: str
    top_bid: Dict[str, float]
    top_ask: Dict[str, float]


@dataclass
class DataPoint:
    """A datapoint from the server."""

    stock: str
    bid_price: float
    ask_price: float
    price: float


def getDataPoint(quote: Quote) -> DataPoint:
    """Produce all the needed values to generate a datapoint"""
    stock = quote["stock"]
    bid_price = float(quote["top_bid"]["price"])
    ask_price = float(quote["top_ask"]["price"])
    price = (bid_price + ask_price) / 2.0
    return DataPoint(stock, bid_price, ask_price, price)


def getRatio(price_a: float, price_b: float) -> Optional[float]:
    """Get ratio of price_a and price_b"""
    if price_b == 0:
        return None
    return price_a / price_b


# Main
if __name__ == "__main__":
    # Query the price once every N seconds.
    for _ in iter(range(N)):
        quotes = json.loads(
            urllib.request.urlopen(QUERY.format(random.random())).read()
        )

        """ ----------- Update to get the ratio --------------- """
        prices = {}
        for quote in quotes:
            data_points = getDataPoint(quote)
            prices[data_points.stock] = data_points.price
            print(
                "Quoted %s at (bid:%s, ask:%s, price:%s)"
                % (
                    data_points.stock,
                    data_points.bid_price,
                    data_points.ask_price,
                    data_points.price,
                )
            )

        print("Ratio %s" % getRatio(prices["ABC"], prices["DEF"]))
