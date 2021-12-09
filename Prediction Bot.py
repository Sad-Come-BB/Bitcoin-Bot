#have a program that takes in three values and finds the 2 slopes and compares it with your data base of other results with leway.
#if there isnt make it take a educated geuss using some trading stragedies from wherever
#   1) Make an array
#   2) get stradgies commonly used
#   3) If there is no solution then 50/50 guess!!!


import trading

endpoint = trading.login("Levis", "LevisT")

side = endpoint.get_btc()
print (side)

    