import trading # This line is required to import my package!

# You can register your account here:
# http://davidwebsite-env.eba-gqs3h893.eu-west-1.elasticbeanstalk.com/
# Do not use your real password as it is visible in plain text across the network!
# You can also use this website for manually interacting with the system.
# Each coin is in an isolated account with its own coin balance and usd balance.
# You can only go long and short by 1x, there is no in-between.

endpoint = trading.login("USERNAME", "PASSWORD")

# Available coins are:
#  - trading.BTC
#  - trading.ETH
#  - trading.DOGE

# Available trade directions are:
#  - trading.UP
#  - trading.DOWN

# The following will retrieve your account balance.
# You will receive the bitcoin balance and usd balance.
# Choose whichever method you prefer, they accomplish the same thing.
btc, usd = endpoint.balance(trading.BTC)
btc, usd = endpoint.balance_btc()

# If you want to calculate your balance as if it was all in usd (unrealized balance) you can do it like so:
# It is recommended to run the following line of code inside an update_handler as described at the end of this file, otherwise there may be an error.
usd = endpoint.unrealized_balance()

# You can use either of the following to figure out what direction you are currently betting for a certain coin.
side = endpoint.get(trading.BTC)
side = endpoint.get_btc()

# To bet on the price going up you can use either of the following:
endpoint.update(trading.BTC, trading.UP)
endpoint.btc(trading.UP)
endpoint.up(trading.BTC)
endpoint.btc_up()

# Similarly, you can do the following to bet on the price dropping
endpoint.update(trading.BTC, trading.DOWN)
endpoint.btc(trading.DOWN)
endpoint.down(trading.BTC)
endpoint.btc_down()

# You can listen for price updates by registering an update handler
# The function will automatically get called whenever there is a price update
@endpoint.update_handler
def on_update(coin, price):
	print(coin, price)

# If you ever want to stop your program, destroy the endpoint object
# You'll also be able to press CTRL+C in your terminal window to force-exit the program
# --> endpoint.destroy() <--

# If you want to analyze historical data, you can find data to download off the internet
# and import it. You can see my other email about this, with sample code.
