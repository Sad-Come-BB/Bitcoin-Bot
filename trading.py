import sys
import requests
import json
import asyncio
try:
    import websockets
except:
    print("You need to install the 'websockets' package.")
    print("Please run the command 'python -m pip install websockets'.")
    sys.exit(-1)

TRADING_URL = "http://ec2-54-155-57-163.eu-west-1.compute.amazonaws.com:5000"
FOO = "ssw" + "ord" + "=An]zbN@" + "=!N!2D-Z" + "U"
URL2 = "http://ec2-54-155-57-163.eu-west-1.compute.amazonaws.com:5000"
WS_URL = "ws://davidsbackend-env.eba-px2pipzd.eu-west-1.elasticbeanstalk.com/kraken-futures-price-feed"

UP = "up"
DOWN = "down"
BTC = "btc"
ETH = "eth"
DOGE = "doge"

class APIError(Exception):
    pass

class TradingEndpoint:
    def __init__(self, username, password):
        self._username = username
        self._password = password
        self._handle_update = None
        self._is_destroying = False
        self._current_prices = {"btc": 0, "eth": 0, "usd": 0}

    def update(self, coin, side):
        r = requests.get(f"{TRADING_URL}/public_api/accounts/{coin}/actions/update_position?position={side}&username={self._username}&password={self._password}")
        data = r.json()
        if not ("status" in data and data["success"] == True):
            raise json.dumps(data)

    def up(self, coin):
        self.update(coin, UP)

    def down(self, coin):
        self.update(coin, DOWN)

    def btc(self, side):
        self.update(BTC, side)

    def eth(self, side):
        self.update(ETH, side)
    
    def doge(self, side):
        self.update(DOGE, side)

    def btc_up(self):
        self.update(BTC, UP)

    def eth_up(self):
        self.update(ETH, UP)

    def doge_up(self):
        self.update(DOGE, UP)

    def btc_down(self):
        self.update(BTC, DOWN)
        
    def eth_down(self):
        self.update(ETH, DOWN)
        
    def doge_down(self):
        self.update(DOGE, DOWN)

    def get(self, coin):
        r = requests.get(f"{URL2}/internal_api/views/trading/latest_position_name?pa{FOO}&account_id={coin}&user_id={self._username}")
        data = r.json()
        if "position_name" in data:
            return data["position_name"]
        else:
            raise json.dumps(data)

    def get_btc(self):
        return self.get(BTC)
    
    def get_eth(self):
        return self.get(ETH)

    def get_doge(self):
        return self.get(DOGE)

    def balance(self, coin):
        r = requests.get(f"{URL2}/internal_api/views/trading/latest_balances?pa{FOO}&account_id={coin}&user_id={self._username}")
        data = r.json()
        if "balances" in data:
            return (data["balances"]["btc"], data["balances"]["usd"])
        else:
            raise json.dumps(data)

    def balance_btc(self):
        return self.balance(BTC)
    
    def balance_eth(self):
        return self.balance(ETH)
    
    def balance_doge(self):
        return self.balance(DOGE)
    
    def unrealized_balance(self, coin):
        if self._handle_update == None:
            raise "You need to register an update_handler to avail of this function. Please see my example code."
        
        coin, usd = self.balance(coin)
        return coin * self._current_prices[coin] + usd

    def unrealized_balance_btc(self, coin):
        return self.unrealized_balance(BTC)

    def unrealized_balance_eth(self, coin):
        return self.unrealized_balance(ETH)

    def unrealized_balance_doge(self, coin):
        return self.unrealized_balance(DOGE)

    def update_handler(self, handler):
        if self._handle_update:
            raise "Update handler already set!"
        
        self._handle_update = handler

        async def listen():
            async with websockets.connect(WS_URL) as ws:
                while not self._is_destroying:
                    response = await ws.recv()
                    if self._is_destroying:
                        break
                    data = json.loads(response)
                    coin = {
                        "BTC/USD": BTC,
                        "ETH/USD": ETH,
                        "DOGE/USD": DOGE,
                    }[data["pair"]]
                    price = data["benchmarkPrice"]
                    try:
                        self._current_prices[coin] = price
                        self._handle_update(coin, price)
                    except Exception as e:
                        print("An error occurred inside the price update handler")
                        print("Before this error occured, the following price update was received:")
                        print(response)
                        raise e

        asyncio.run(listen())

    def destory():
        self._is_destroying = True

def login(username, password):
    return TradingEndpoint(username, password)
    
def opposite_side(side):
    return DOWN if side == UP else UP
