# btcBOT
Bitcoin Automated Trading Bot 🚀
Overview
A powerful, intelligent Bitcoin trading bot that uses seasonal patterns, technical analysis, and risk management to automate BTC/USDT trading. Perfect for short-term trading strategies with built-in paper trading mode for safe testing.

🌟 Key Features
1. Seasonal Pattern Analysis
Uses historical Bitcoin monthly performance data (2009-2025)

Automatically adjusts trading strategy based on current month

Best Months: November (35.51%), April (33.79%), October (25%)

Worst Months: September (-4.67%), August (-0.07%)

2. Advanced Technical Indicators
RSI (Relative Strength Index): Identifies overbought/oversold conditions

MACD (Moving Average Convergence Divergence): Detects trend changes

Bollinger Bands: Measures volatility and price extremes

Volume Analysis: Confirms trading signals

3. Smart Risk Management
Uses only 20% of available funds per trade

Prevents over-leveraging

Protects capital during volatile periods

4. Paper Trading Mode
Test strategies with $10,000 virtual money

Risk-free environment

Real-time market data

Perfect for learning and optimization

5. Flexible Configuration
Set maximum number of trades OR run indefinitely

Adjustable check intervals (default: 5 minutes)

Easy switch between paper and live trading

6. Beautiful Interface
Color-coded console output

Real-time portfolio tracking

Clear buy/sell signals

Performance metrics

📦 Installation
Step 1: Install Python
Make sure you have Python 3.8+ installed on your system.

Step 2: Install Required Libraries
bash
pip install -r requirements.txt
Or install manually:

bash
pip install ccxt pandas numpy ta colorama
🚀 Quick Start
Run in Paper Trading Mode (Recommended for Beginners)
bash
python bitcoin_trading_bot.py
Customize Settings
Edit the main() function in bitcoin_trading_bot.py:
