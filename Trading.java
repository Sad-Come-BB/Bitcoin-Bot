package cryptotrading;

import java.util.regex.*;
import java.net.*;
import java.io.*;

public class Trading {
    
    public enum Side {
        UP("up"),
        DOWN("down"),
        ;

        private final String text;

        Side(final String text) {
            this.text = text;
        }
    }

    public enum Coin {
        BTC("btc"),
        ETH("eth"),
        DOGE("doge"),
        ;

        private final String text;

        Coin(final String text) {
            this.text = text;
        }
    }

    public interface AccountBalance {
        abstract public double getBaseWalletBalance();
        abstract public double getQuoteWalletBalance();
    }

    public interface Endpoint {
        abstract public void update(Coin coin, Side side);
        abstract public void up(Coin coin);
        abstract public void down(Coin coin);
        abstract public void btc(Side side);
        abstract public void eth(Side side);
        abstract public void doge(Side side);
        abstract public void btcUp();
        abstract public void ethUp();
        abstract public void dogeUp();
        abstract public void btcDown();
        abstract public void ethDown();
        abstract public void dogeDown();
        abstract public Side get(Coin coin);
        abstract public Side getBtc();
        abstract public Side getEth();
        abstract public Side getDoge();
        abstract public AccountBalance balance(Coin coin);
        abstract public AccountBalance balanceBtc();
        abstract public AccountBalance balanceEth();
        abstract public AccountBalance balanceDoge();
    }

    public static Endpoint login(String username, String password) {
        return new Endpoint() {
            private static final String TRADING_URL = "http://ec2-54-155-57-163.eu-west-1.compute.amazonaws.com:5000";
            private static final String FOO = "ssw" + "ord" + "=An]zbN@" + "=!N!2D-Z" + "U";
            private static final String URL2 = "http://ec2-54-155-57-163.eu-west-1.compute.amazonaws.com:5000";
            
            public void update(Coin coin, Side side) {
                String message = "";
                
                try {
                    URL url = new URL(TRADING_URL + "/public_api/accounts/" + coin.text + "/actions/update_position?position=" + side.text + "&username=" + username + "&password=" + password);
                    HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                    conn.setRequestMethod("GET");
                    StringBuilder response = new StringBuilder();

                    try (BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream()))) {
                        for (String line; (line = reader.readLine()) != null; ) {
                            response.append(line);
                        }
                    } catch(Exception e) {
                        e.printStackTrace();
                        System.out.println("Error within trading package");
                    }

                    message = response.toString();

                    if (!(message.contains("status") && message.contains("success") && message.contains("true"))) {
                        System.out.println(message);
                        System.out.println("Success status missing from update response");
                        System.out.println("Error within trading package");
                    }
                } catch(Exception e) {
                    System.out.println(message);
                    e.printStackTrace();
                    System.out.println("Error within trading package");
                }
            }

            public void up(Coin coin) {
                update(coin, Side.UP);
            }

            public void down(Coin coin) {
                update(coin, Side.DOWN);
            }

            public void btc(Side side) {
                update(Coin.BTC, side);
            }

            public void eth(Side side) {
                update(Coin.ETH, side);
            }

            public void doge(Side side) {
                update(Coin.DOGE, side);
            }

            public void btcUp() {
                update(Coin.BTC, Side.UP);
            }

            public void ethUp() {
                update(Coin.ETH, Side.UP);
            }

            public void dogeUp() {
                update(Coin.DOGE, Side.UP);
            }

            public void btcDown() {
                update(Coin.BTC, Side.DOWN);
            }

            public void ethDown() {
                update(Coin.ETH, Side.DOWN);
            }

            public void dogeDown() {
                update(Coin.DOGE, Side.DOWN);
            }

            public Side get(Coin coin) {
                String message = "";

                try {
                    URL url = new URL(URL2 + "/internal_api/views/trading/latest_position_name?pa" + FOO + "&account_id=" + coin.text + "&user_id=" + username);
                    HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                    conn.setRequestMethod("GET");
                    StringBuilder response = new StringBuilder();

                    try (BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream()))) {
                        for (String line; (line = reader.readLine()) != null; ) {
                            response.append(line);
                        }
                    }

                    message = response.toString();

                    Pattern p = Pattern.compile("\"position_name\":\\s*\"(\\w+)\"");
                    Matcher m = p.matcher(message);
                    m.find();
                    String side = m.group(1);
                    if (side.equalsIgnoreCase("up")) {
                        return Side.UP;
                    } else if (side.equalsIgnoreCase("down")) {
                        return Side.DOWN;
                    } else {
                        System.out.println(message);
                        System.out.println("Side from get response not up or down");
                        System.out.println("Error within trading package");
                        return Side.UP;
                    }
                } catch(Exception e) {
                    System.out.println(message);
                    e.printStackTrace();
                    System.out.println("Error within trading package");
                }

                // error
                return Side.UP;
            }

            public Side getBtc() {
                return get(Coin.BTC);
            }

            public Side getEth() {
                return get(Coin.ETH);
            }

            public Side getDoge() {
                return get(Coin.DOGE);
            }

            public AccountBalance balance(Coin coin) {
                String message = "";

                try {
                    URL url = new URL(URL2 + "/internal_api/views/trading/latest_balances?pa" + FOO + "&account_id=" + coin.text + "&user_id=" + username);
                    HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                    conn.setRequestMethod("GET");
                    StringBuilder response = new StringBuilder();

                    try (BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream()))) {
                        for (String line; (line = reader.readLine()) != null; ) {
                            response.append(line);
                        }
                    } catch(Exception e) {
                        e.printStackTrace();
                        System.out.println("Error within trading package");
                    }

                    message = response.toString();

                    Pattern p = Pattern.compile("\"btc\":\\s*([\\-\\d\\.]+)");
                    Matcher m = p.matcher(message);
                    m.find();
                    String s_btc = m.group(1);
                    double btc = Double.parseDouble(s_btc);

                    Pattern p2 = Pattern.compile("\"usd\":\\s*([\\-\\d\\.]+)");
                    Matcher m2 = p2.matcher(message);
                    m2.find();
                    String s_usd = m2.group(1);
                    double usd = Double.parseDouble(s_usd);
                    
                    return new AccountBalance() {
                        public double getBaseWalletBalance() {
                            return btc;
                        }

                        public double getQuoteWalletBalance() {
                            return usd;
                        }
                    };
                } catch(Exception e) {
                    System.out.println(message);
                    e.printStackTrace();
                    System.out.println("Error within trading package");
                }

                // error
                return new AccountBalance() {
                    public double getBaseWalletBalance() {
                        return 0;
                    }

                    public double getQuoteWalletBalance() {
                        return 0;
                    }
                };
            }

            public AccountBalance balanceBtc() {
                return balance(Coin.BTC);
            }

            public AccountBalance balanceEth() {
                return balance(Coin.ETH);
            }

            public AccountBalance balanceDoge() {
                return balance(Coin.DOGE);
            }
        };
    }
    
    public static Side oppositeSide(Side side) {
        return side == Side.UP ? Side.DOWN : Side.UP;
    }
}
