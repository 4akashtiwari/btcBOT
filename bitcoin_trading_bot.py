"""
BITCOIN AUTOMATED TRADING BOT
================================
Features:
- Seasonal pattern analysis based on historical data
- Multiple technical indicators (RSI, MACD, Bollinger Bands)
- Paper trading mode for testing
- Risk management (20% fund allocation)
- Configurable trade frequency
- Cool colorful interface
"""

import ccxt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import ta
from colorama import Fore, Back, Style, init
import json
import os

# Initialize colorama for colored output
init(autoreset=True)

class BitcoinTradingBot:
    def __init__(self, api_key=None, api_secret=None, paper_trading=True):
        """
        Initialize the Bitcoin Trading Bot

        Parameters:
        - api_key: Exchange API key (optional for paper trading)
        - api_secret: Exchange API secret (optional for paper trading)
        - paper_trading: Set to True for paper trading mode
        """
        self.paper_trading = paper_trading
        self.api_key = api_key
        self.api_secret = api_secret

        # Initialize exchange (Binance Testnet for paper trading)
        if paper_trading:
            self.exchange = ccxt.binance({
                'enableRateLimit': True,
                'options': {'defaultType': 'spot'}
            })
            self.print_info("📄 PAPER TRADING MODE ACTIVATED")
        else:
            self.exchange = ccxt.binance({
                'apiKey': api_key,
                'secret': api_secret,
                'enableRateLimit': True,
                'options': {'defaultType': 'spot'}
            })
            self.print_info("💰 LIVE TRADING MODE ACTIVATED")

        # Trading parameters
        self.symbol = 'BTC/USDT'
        self.timeframe = '15m'  # 15-minute candles for short-term trading
        self.allocation_percent = 0.20  # Use only 20% of funds

        # Technical indicator parameters
        self.rsi_period = 14
        self.rsi_overbought = 70
        self.rsi_oversold = 30
        self.macd_fast = 12
        self.macd_slow = 26
        self.macd_signal = 9
        self.bb_period = 20
        self.bb_std = 2

        # Paper trading portfolio
        self.paper_balance = {
            'USDT': 10000.0,  # Starting with $10,000
            'BTC': 0.0
        }

        # Trading history
        self.trades = []
        self.trade_count = 0
        self.max_trades = None  # None for infinite

        # Monthly seasonality data (from research)
        self.monthly_multipliers = {
            1: 0.95,   # January (9.74%)
            2: 1.0,    # February (12.52%)
            3: 0.95,   # March (9.19%)
            4: 1.3,    # April (33.79%) - BEST MONTH
            5: 1.1,    # May (17.82%)
            6: 0.9,    # June (7.76%)
            7: 0.9,    # July (7.36%)
            8: 0.7,    # August (-0.07%) - WORST
            9: 0.6,    # September (-4.67%) - WORST
            10: 1.2,   # October (25%)
            11: 1.3,   # November (35.51%) - BEST MONTH
            12: 1.0    # December (10.45%)
        }

        self.print_banner()

    def print_banner(self):
        """Print welcome banner"""
        print(Fore.CYAN + Style.BRIGHT + "="*80)
        print(Fore.YELLOW + Style.BRIGHT + """
        ╔══════════════════════════════════════════════════════════════╗
        ║                                                              ║
        ║        🚀 BITCOIN AUTOMATED TRADING BOT v1.0 🚀             ║
        ║                                                              ║
        ║        Powered by AI & Seasonal Pattern Analysis            ║
        ║                                                              ║
        ╚══════════════════════════════════════════════════════════════╝
        """)
        print(Fore.CYAN + Style.BRIGHT + "="*80)

    def print_success(self, message):
        """Print success message in green"""
        print(Fore.GREEN + Style.BRIGHT + "✅ " + message)

    def print_error(self, message):
        """Print error message in red"""
        print(Fore.RED + Style.BRIGHT + "❌ " + message)

    def print_warning(self, message):
        """Print warning message in yellow"""
        print(Fore.YELLOW + Style.BRIGHT + "⚠️  " + message)

    def print_info(self, message):
        """Print info message in cyan"""
        print(Fore.CYAN + Style.BRIGHT + "ℹ️  " + message)

    def print_trade(self, message):
        """Print trade message in magenta"""
        print(Fore.MAGENTA + Style.BRIGHT + "💹 " + message)

    def fetch_ohlcv(self, limit=100):
        """Fetch OHLCV data for analysis"""
        try:
            ohlcv = self.exchange.fetch_ohlcv(self.symbol, self.timeframe, limit=limit)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            return df
        except Exception as e:
            self.print_error(f"Error fetching data: {e}")
            return None

    def calculate_indicators(self, df):
        """Calculate technical indicators"""
        # RSI
        df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=self.rsi_period).rsi()

        # MACD
        macd = ta.trend.MACD(df['close'], 
                            window_slow=self.macd_slow,
                            window_fast=self.macd_fast,
                            window_sign=self.macd_signal)
        df['macd'] = macd.macd()
        df['macd_signal'] = macd.macd_signal()
        df['macd_diff'] = macd.macd_diff()

        # Bollinger Bands
        bb = ta.volatility.BollingerBands(df['close'], 
                                         window=self.bb_period,
                                         window_dev=self.bb_std)
        df['bb_upper'] = bb.bollinger_hband()
        df['bb_middle'] = bb.bollinger_mavg()
        df['bb_lower'] = bb.bollinger_lband()

        # Volume analysis
        df['volume_sma'] = df['volume'].rolling(window=20).mean()

        return df

    def get_seasonal_factor(self):
        """Get seasonal multiplier for current month"""
        current_month = datetime.now().month
        return self.monthly_multipliers.get(current_month, 1.0)

    def generate_signal(self, df):
        """
        Generate trading signal based on multiple indicators
        Returns: 'BUY', 'SELL', or 'HOLD'
        """
        if df is None or len(df) < 50:
            return 'HOLD'

        latest = df.iloc[-1]
        prev = df.iloc[-2]

        # Get seasonal factor
        seasonal_factor = self.get_seasonal_factor()
        current_month = datetime.now().strftime("%B")

        # Initialize signal score
        buy_score = 0
        sell_score = 0

        # RSI Analysis
        if latest['rsi'] < self.rsi_oversold:
            buy_score += 2  # Strong buy signal
            self.print_info(f"RSI Oversold: {latest['rsi']:.2f}")
        elif latest['rsi'] < 40:
            buy_score += 1  # Moderate buy signal
        elif latest['rsi'] > self.rsi_overbought:
            sell_score += 2  # Strong sell signal
            self.print_info(f"RSI Overbought: {latest['rsi']:.2f}")
        elif latest['rsi'] > 60:
            sell_score += 1  # Moderate sell signal

        # MACD Analysis
        if latest['macd'] > latest['macd_signal'] and prev['macd'] <= prev['macd_signal']:
            buy_score += 2  # Bullish crossover
            self.print_info("MACD Bullish Crossover")
        elif latest['macd'] < latest['macd_signal'] and prev['macd'] >= prev['macd_signal']:
            sell_score += 2  # Bearish crossover
            self.print_info("MACD Bearish Crossover")

        # Bollinger Bands Analysis
        if latest['close'] < latest['bb_lower']:
            buy_score += 1  # Price below lower band
            self.print_info("Price below lower Bollinger Band")
        elif latest['close'] > latest['bb_upper']:
            sell_score += 1  # Price above upper band
            self.print_info("Price above upper Bollinger Band")

        # Volume Analysis
        if latest['volume'] > latest['volume_sma'] * 1.5:
            # High volume confirms signal
            if buy_score > sell_score:
                buy_score += 1
            elif sell_score > buy_score:
                sell_score += 1

        # Apply seasonal factor
        self.print_info(f"Current Month: {current_month} (Seasonal Factor: {seasonal_factor:.2f}x)")
        buy_score = buy_score * seasonal_factor

        # Determine final signal
        if buy_score >= 4 and buy_score > sell_score:
            return 'BUY'
        elif sell_score >= 4 and sell_score > buy_score:
            return 'SELL'
        else:
            return 'HOLD'

    def execute_trade(self, signal, current_price):
        """Execute trade based on signal"""
        if signal == 'HOLD':
            return

        # Check if we've reached max trades
        if self.max_trades and self.trade_count >= self.max_trades:
            self.print_warning("Maximum number of trades reached!")
            return

        if self.paper_trading:
            self.execute_paper_trade(signal, current_price)
        else:
            self.execute_live_trade(signal, current_price)

    def execute_paper_trade(self, signal, current_price):
        """Execute paper trade"""
        if signal == 'BUY':
            # Calculate position size (20% of USDT balance)
            usdt_to_spend = self.paper_balance['USDT'] * self.allocation_percent

            if usdt_to_spend < 10:  # Minimum $10
                self.print_warning("Insufficient USDT balance for trade")
                return

            btc_amount = usdt_to_spend / current_price
            self.paper_balance['BTC'] += btc_amount
            self.paper_balance['USDT'] -= usdt_to_spend

            trade_info = {
                'timestamp': datetime.now(),
                'type': 'BUY',
                'price': current_price,
                'amount': btc_amount,
                'value': usdt_to_spend
            }
            self.trades.append(trade_info)
            self.trade_count += 1

            self.print_trade(f"BUY ORDER EXECUTED")
            self.print_success(f"Bought {btc_amount:.6f} BTC at ${current_price:.2f}")
            self.print_success(f"Total Cost: ${usdt_to_spend:.2f}")

        elif signal == 'SELL':
            # Sell 20% of BTC holdings
            btc_to_sell = self.paper_balance['BTC'] * self.allocation_percent

            if btc_to_sell < 0.0001:  # Minimum BTC amount
                self.print_warning("Insufficient BTC balance for trade")
                return

            usdt_received = btc_to_sell * current_price
            self.paper_balance['BTC'] -= btc_to_sell
            self.paper_balance['USDT'] += usdt_received

            trade_info = {
                'timestamp': datetime.now(),
                'type': 'SELL',
                'price': current_price,
                'amount': btc_to_sell,
                'value': usdt_received
            }
            self.trades.append(trade_info)
            self.trade_count += 1

            self.print_trade(f"SELL ORDER EXECUTED")
            self.print_success(f"Sold {btc_to_sell:.6f} BTC at ${current_price:.2f}")
            self.print_success(f"Total Received: ${usdt_received:.2f}")

        self.display_portfolio()

    def execute_live_trade(self, signal, current_price):
        """Execute live trade (placeholder - implement with caution)"""
        self.print_warning("Live trading not fully implemented. Use paper trading mode.")
        # Implement live trading logic here with proper error handling
        pass

    def display_portfolio(self):
        """Display current portfolio status"""
        total_value = self.paper_balance['USDT'] + (self.paper_balance['BTC'] * self.get_current_price())
        initial_value = 10000.0
        profit_loss = total_value - initial_value
        profit_loss_percent = (profit_loss / initial_value) * 100

        print(Fore.CYAN + Style.BRIGHT + "\n" + "="*60)
        print(Fore.YELLOW + Style.BRIGHT + "           📊 CURRENT PORTFOLIO STATUS 📊")
        print(Fore.CYAN + Style.BRIGHT + "="*60)
        print(Fore.WHITE + f"  USDT Balance:  ${self.paper_balance['USDT']:.2f}")
        print(Fore.WHITE + f"  BTC Balance:   {self.paper_balance['BTC']:.6f} BTC")
        print(Fore.WHITE + f"  Total Value:   ${total_value:.2f}")
        print(Fore.WHITE + f"  Profit/Loss:   ", end="")

        if profit_loss >= 0:
            print(Fore.GREEN + Style.BRIGHT + f"${profit_loss:.2f} (+{profit_loss_percent:.2f}%)")
        else:
            print(Fore.RED + Style.BRIGHT + f"${profit_loss:.2f} ({profit_loss_percent:.2f}%)")

        print(Fore.WHITE + f"  Total Trades:  {self.trade_count}")
        print(Fore.CYAN + Style.BRIGHT + "="*60 + "\n")

    def get_current_price(self):
        """Get current BTC price"""
        try:
            ticker = self.exchange.fetch_ticker(self.symbol)
            return ticker['last']
        except Exception as e:
            self.print_error(f"Error fetching price: {e}")
            return 0

    def save_results(self):
        """Save trading results to file"""
        results = {
            'final_balance': self.paper_balance,
            'trades': [
                {
                    'timestamp': t['timestamp'].strftime('%Y-%m-%d %H:%M:%S'),
                    'type': t['type'],
                    'price': t['price'],
                    'amount': t['amount'],
                    'value': t['value']
                }
                for t in self.trades
            ]
        }

        with open('trading_results.json', 'w') as f:
            json.dump(results, f, indent=4)

        self.print_success("Results saved to trading_results.json")

    def run(self, max_trades=None, check_interval=300):
        """
        Run the trading bot

        Parameters:
        - max_trades: Maximum number of trades (None for infinite)
        - check_interval: Time between checks in seconds (default 300 = 5 minutes)
        """
        self.max_trades = max_trades

        if max_trades:
            self.print_info(f"Bot will execute maximum {max_trades} trades")
        else:
            self.print_info("Bot will run indefinitely (infinite trades)")

        self.print_info(f"Checking market every {check_interval} seconds")
        self.print_info(f"Using {self.allocation_percent*100}% of available funds per trade")
        print()

        try:
            iteration = 0
            while True:
                iteration += 1

                # Check if we've reached max trades
                if self.max_trades and self.trade_count >= self.max_trades:
                    self.print_success("Maximum trades reached. Stopping bot.")
                    break

                print(Fore.BLUE + Style.BRIGHT + f"\n{'='*60}")
                print(Fore.BLUE + Style.BRIGHT + f"  Iteration #{iteration} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print(Fore.BLUE + Style.BRIGHT + f"{'='*60}\n")

                # Fetch market data
                self.print_info("Fetching market data...")
                df = self.fetch_ohlcv(limit=100)

                if df is not None:
                    # Calculate indicators
                    df = self.calculate_indicators(df)

                    # Get current price
                    current_price = df.iloc[-1]['close']
                    self.print_info(f"Current BTC Price: ${current_price:.2f}")

                    # Generate signal
                    signal = self.generate_signal(df)

                    if signal == 'BUY':
                        print(Fore.GREEN + Style.BRIGHT + "\n🔔 SIGNAL: BUY 🔔\n")
                    elif signal == 'SELL':
                        print(Fore.RED + Style.BRIGHT + "\n🔔 SIGNAL: SELL 🔔\n")
                    else:
                        print(Fore.YELLOW + Style.BRIGHT + "\n🔔 SIGNAL: HOLD 🔔\n")

                    # Execute trade
                    self.execute_trade(signal, current_price)

                # Wait for next iteration
                if not (self.max_trades and self.trade_count >= self.max_trades):
                    self.print_info(f"Waiting {check_interval} seconds until next check...\n")
                    time.sleep(check_interval)

        except KeyboardInterrupt:
            print()
            self.print_warning("Bot stopped by user")
        except Exception as e:
            self.print_error(f"Error: {e}")
        finally:
            self.display_portfolio()
            self.save_results()
            print(Fore.CYAN + Style.BRIGHT + "\nThank you for using Bitcoin Trading Bot! 👋\n")


def main():
    """Main function to run the bot"""
    print(Fore.CYAN + Style.BRIGHT + "\n" + "="*80)
    print(Fore.YELLOW + Style.BRIGHT + "        BITCOIN AUTOMATED TRADING BOT - CONFIGURATION")
    print(Fore.CYAN + Style.BRIGHT + "="*80 + "\n")

    # Configuration
    paper_trading = True  # Set to False for live trading (with proper API keys)

    # Initialize bot
    bot = BitcoinTradingBot(paper_trading=paper_trading)

    # Run bot
    # Options:
    # 1. Infinite trades: bot.run(max_trades=None, check_interval=300)
    # 2. Limited trades: bot.run(max_trades=10, check_interval=300)

    bot.run(max_trades=10, check_interval=60)  # 10 trades, check every 60 seconds


if __name__ == "__main__":
    main()
