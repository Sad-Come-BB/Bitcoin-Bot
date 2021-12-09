import cryptotrading.*; // This line is required to import my package!
// HOWEVER! Remove the above line if using BlueJ !!!

public class Example {
	public static void main(String[] args) {
		// You can register your account here:
		// http://davidwebsite-env.eba-gqs3h893.eu-west-1.elasticbeanstalk.com/
		// Do not use your real password as it is visible in plain text across the network!
		// You can also use this website for manually interacting with the system.
		// Each coin is in an isolated account with its own coin balance and usd balance.
		// You can only go long and short by 1x, there is no in-between.
		
		Trading.Endpoint endpoint = Trading.login("username", "password");

		// Available coins are:
		//  - Trading.Coin.BTC
		//  - Trading.Coin.ETH
		//  - Trading.Coin.DOG
		
		// Available trade directions are:
		//  - Trading.Side.UP
		//  - Trading.Side.DOWN

		// The following will retrieve your account balance.
		// Choose whichever method you prefer, they accomplish the same thing.
		Trading.AccountBalance bal  = endpoint.balance(Trading.Coin.BTC);
		Trading.AccountBalance bal_ = endpoint.balanceBtc();

		// You will receive the bitcoin balance and usd balance, which can be extracted like so:
		double btc = bal.getBaseWalletBalance();
		double usd = bal.getQuoteWalletBalance();
		
		// If you want to calculate your balance as if it was all in usd, you must calculate it like so:
		double currentBitcoinPrice = 65000; // it is your responsibility to update this variable dynamically based on some price feed / price source
		double accountBalanceAsIfItWasInUsd = btc * currentBitcoinPrice + usd;
		
		// You can use either of the following to figure out what direction you are currently betting for a certain coin.
		Trading.Side side  = endpoint.get(Trading.Coin.BTC);
		Trading.Side side_ = endpoint.getBtc();
		
		// To bet on the price going up you can use either of the following:
		endpoint.update(Trading.Coin.BTC, Trading.Side.UP);
		endpoint.btc(Trading.Side.UP);
		endpoint.up(Trading.Coin.BTC);
		endpoint.btcUp();
		
		// Similarly, you can do the following to bet on the price dropping
		endpoint.update(Trading.Coin.BTC, Trading.Side.DOWN);
		endpoint.btc(Trading.Side.DOWN);
		endpoint.down(Trading.Coin.BTC);
		endpoint.btcDown();
	}
}
