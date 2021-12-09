import time
print ("Darragh gay")

time.sleep(3)
print ("jk no he a tranny")


@endpoint.update_handler
def on_update(coin, price):
    if (coin == trading.BTC):
        print (coin,price)
        time.sleep(300)


