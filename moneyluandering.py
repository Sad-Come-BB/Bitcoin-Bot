#    Look at Oscillators   [do this next??]
import time 
import trading
from dataclasses import dataclass


@dataclass
class Period:
    timestamp: int = None
    open: float = None
    high: float = None
    low: float = None
    close: float = None
    newclose: float = None
    mid: float = None
    avg: float = None

endpoint = trading.login("CS225LevisT", "levis")

btc, myprice = endpoint.balance_btc()
side = endpoint.get_btc()
    
def up():
    global side
    if side != trading.UP:
        side = trading.UP
        endpoint.up(trading.BTC)

def down():
    global side
    if side != trading.DOWN:
        side = trading.DOWN
        endpoint.down(trading.BTC)

f = open("Binance_BTCUSDT_minute.csv")
#f = open("Minute one")
data = f.readlines()[2:]
f.close()



def checkpattern(newprecent):
    up = 0
    down = 0
  
    for i in reversed(range(len(data)-1)):
        line = data[i+1]
        nextline = data[i]
        segments = line.split(",")
        period = Period()
        period.open = float(segments[3])
        period.close = float(segments[6])
        old_precent = (period.open-period.close)/(period.open)
       
        next_segments = nextline.split(",")
        period.newclose = float(next_segments[6])
        idk = (period.close-period.newclose)/(period.close)
        #change to precentages, close-open/open
        if (old_precent-0.0009 < newprecent < old_precent+0.0009) and newprecent < (idk):
            down+=1
        if (old_precent-0.0009 < newprecent < old_precent+0.0009) and newprecent > (idk):
            up+=1
    print ("down:", down)
    print ("up:", up)  
    print ("checked csv file")
    if up == down:
        return "null"
    if up > down:
        return "UP"
    elif down > up:
        return "DOWN"

first_price_time = time.time()
first_price = None
@endpoint.update_handler
def on_update(coin, price):
    global first_price_time, first_price,change_in_price
    
    if coin == trading.BTC:
        if first_price == None:
            first_price = price

    current_time = time.time()
    dt = current_time - first_price_time
    
    if dt > 45:
        first_price_time = current_time
        change_in_price = price - first_price
        percentage = (change_in_price / first_price)
    
        vote = checkpattern(percentage)
    
        if vote == "UP":
            up()
            print ("voted up")
        if vote == "DOWN":
            down()
            print ("voted down")
        if vote == "null":
            side = endpoint.get_btc()
            if side == "up":
                up()
                print ("voted up")
            if side == "down":
                down()
                print ("voted down")
            
    
    
