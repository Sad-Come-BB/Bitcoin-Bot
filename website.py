import trading

endpoint = trading.login("Levis", "LevisT")

btc, myprice = endpoint.balance_btc()

print (btc,myprice)

actual = btc * 58161 + myprice
print(actual)

side = endpoint.get(trading.BTC)

def up():
    if side != trading.UP:
        side = trading.UP
        endpoint.up(trading.BTC)

def down():
    if side != trading.DOWN:
        side = trading.DOWN
        endpoint.down(trading.BTC)

@endpoint.update_handler
def on_update(coin, price):
    print(coin, price)
    if coin == trading.BTC:

        if 57000<=price<=58200:
            up()
            print ("voted down")
        if 58201<=price<=58500:
            down()
            print ("voted up")
