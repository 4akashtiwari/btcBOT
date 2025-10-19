# Bitcoin Automated Trading Bot 🚀

## Overview
A powerful, intelligent Bitcoin trading bot that uses seasonal patterns, technical analysis, and risk management to automate BTC/USDT trading. Perfect for short-term trading strategies with built-in paper trading mode for safe testing.

## 🌟 Key Features

### 1. **Seasonal Pattern Analysis**
- Uses historical Bitcoin monthly performance data (2009-2025)
- Automatically adjusts trading strategy based on current month
- **Best Months**: November (35.51%), April (33.79%), October (25%)
- **Worst Months**: September (-4.67%), August (-0.07%)

### 2. **Advanced Technical Indicators**
- **RSI (Relative Strength Index)**: Identifies overbought/oversold conditions
- **MACD (Moving Average Convergence Divergence)**: Detects trend changes
- **Bollinger Bands**: Measures volatility and price extremes
- **Volume Analysis**: Confirms trading signals

### 3. **Smart Risk Management**
- Uses only 20% of available funds per trade
- Prevents over-leveraging
- Protects capital during volatile periods

### 4. **Paper Trading Mode**
- Test strategies with $10,000 virtual money
- Risk-free environment
- Real-time market data
- Perfect for learning and optimization

### 5. **Flexible Configuration**
- Set maximum number of trades OR run indefinitely
- Adjustable check intervals (default: 5 minutes)
- Easy switch between paper and live trading

### 6. **Beautiful Interface**
- Color-coded console output
- Real-time portfolio tracking
- Clear buy/sell signals
- Performance metrics

## 📦 Installation

### Step 1: Install Python
Make sure you have Python 3.8+ installed on your system.

### Step 2: Install Required Libraries
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install ccxt pandas numpy ta colorama
```

## 🚀 Quick Start

### Run in Paper Trading Mode (Recommended for Beginners)
```bash
python bitcoin_trading_bot.py
```

### Customize Settings
Edit the `main()` function in `bitcoin_trading_bot.py`:

```python
# For 10 trades with 60-second intervals
bot.run(max_trades=10, check_interval=60)

# For infinite trades with 5-minute intervals
bot.run(max_trades=None, check_interval=300)

# For testing: 5 trades with 30-second intervals
bot.run(max_trades=5, check_interval=30)
```

## 📊 How It Works

### Trading Algorithm

1. **Fetch Market Data**: Downloads recent Bitcoin price data (15-minute candles)

2. **Calculate Indicators**:
   - RSI (14-period)
   - MACD (12, 26, 9)
   - Bollinger Bands (20-period, 2 std dev)

3. **Generate Signal**:
   - Analyzes all indicators
   - Applies seasonal adjustment
   - Assigns buy/sell scores
   - Returns BUY, SELL, or HOLD

4. **Execute Trade**:
   - BUY: Uses 20% of USDT balance
   - SELL: Sells 20% of BTC holdings
   - Updates portfolio

5. **Repeat**: Waits for check_interval and repeats

### Signal Generation Logic

**BUY Signal (Score >= 4)**:
- RSI < 30 (oversold) = +2 points
- MACD bullish crossover = +2 points
- Price below lower Bollinger Band = +1 point
- High volume confirmation = +1 point
- Multiplied by seasonal factor

**SELL Signal (Score >= 4)**:
- RSI > 70 (overbought) = +2 points
- MACD bearish crossover = +2 points
- Price above upper Bollinger Band = +1 point
- High volume confirmation = +1 point

**HOLD**: Score < 4 or conflicting signals

## 📈 Monthly Seasonality Data

Based on 15+ years of historical Bitcoin data:

| Month     | Avg Return | Strategy         |
|-----------|------------|------------------|
| January   | 9.74%      | Hold/Caution     |
| February  | 12.52%     | Buy Period       |
| March     | 9.19%      | Hold/Caution     |
| April     | 33.79%     | **Strong Buy**   |
| May       | 17.82%     | Buy Period       |
| June      | 7.76%      | Hold/Caution     |
| July      | 7.36%      | Hold/Caution     |
| August    | -0.07%     | Sell/Avoid       |
| September | -4.67%     | **Sell/Avoid**   |
| October   | 25.00%     | Buy Period       |
| November  | 35.51%     | **Strong Buy**   |
| December  | 10.45%     | Buy Period       |

## 🎨 Interface Features

The bot uses color-coded output for easy reading:
- 🟢 **Green**: Success messages, buy signals
- 🔴 **Red**: Error messages, sell signals
- 🟡 **Yellow**: Warnings, hold signals
- 🔵 **Cyan**: Information, system messages
- 🟣 **Magenta**: Trade executions

## 📁 Output Files

### trading_results.json
Contains complete trading history:
```json
{
    "final_balance": {
        "USDT": 10234.56,
        "BTC": 0.123456
    },
    "trades": [
        {
            "timestamp": "2025-10-19 16:30:00",
            "type": "BUY",
            "price": 67500.00,
            "amount": 0.029629,
            "value": 2000.00
        }
    ]
}
```

### bitcoin_monthly_seasonality.csv
Historical seasonal pattern data for analysis

## ⚙️ Configuration Options

### In the Bot Class:

```python
# Trading pair
self.symbol = 'BTC/USDT'

# Timeframe for candlesticks
self.timeframe = '15m'  # Options: 1m, 5m, 15m, 1h, 4h, 1d

# Fund allocation per trade
self.allocation_percent = 0.20  # 20% of available funds

# RSI parameters
self.rsi_period = 14
self.rsi_overbought = 70
self.rsi_oversold = 30

# MACD parameters
self.macd_fast = 12
self.macd_slow = 26
self.macd_signal = 9

# Bollinger Bands parameters
self.bb_period = 20
self.bb_std = 2

# Paper trading starting balance
self.paper_balance = {
    'USDT': 10000.0,
    'BTC': 0.0
}
```

## 🔐 Live Trading Setup (Advanced)

⚠️ **WARNING**: Live trading involves real money. Test thoroughly in paper mode first!

1. Create a Binance account and generate API keys
2. Enable spot trading permissions (NOT futures/margin)
3. Set API key restrictions (IP whitelist recommended)
4. Update bot initialization:

```python
bot = BitcoinTradingBot(
    api_key='YOUR_API_KEY',
    api_secret='YOUR_API_SECRET',
    paper_trading=False  # ENABLE LIVE TRADING
)
```

## 📚 Learning Resources

### Successful Trading Strategies Implemented:
- **Mean Reversion**: Buy oversold, sell overbought
- **Momentum Trading**: Follow strong trends
- **Seasonal Patterns**: Trade during favorable months
- **Volume Confirmation**: Verify signals with volume

### Technical Indicators Explained:
- **RSI**: Measures momentum (0-100 scale)
- **MACD**: Shows trend direction and strength
- **Bollinger Bands**: Indicates volatility and extremes

## 🛡️ Risk Management

1. **20% Position Sizing**: Never risks more than 20% per trade
2. **Diversified Signals**: Uses multiple indicators to confirm trades
3. **Seasonal Adjustment**: Reduces exposure during historically poor months
4. **Paper Trading First**: Test before risking real money

## 🐛 Troubleshooting

### "Error fetching data"
- Check internet connection
- Verify exchange is accessible
- Try increasing check_interval

### "Insufficient balance"
- Increase paper_balance starting amount
- Reduce allocation_percent
- Check minimum trade amounts

### "Rate limit exceeded"
- Increase check_interval (minimum 60 seconds recommended)
- Enable rate limiting in exchange settings

## 📝 Best Practices

1. **Start with Paper Trading**: Test for at least 1-2 weeks
2. **Monitor Performance**: Review trading_results.json regularly
3. **Adjust Parameters**: Fine-tune based on market conditions
4. **Risk Management**: Never invest more than you can afford to lose
5. **Stay Informed**: Keep up with Bitcoin news and market trends
6. **Backtest**: Use historical data to validate strategy

## 🔄 Customization Ideas

### Add Stop-Loss:
```python
def check_stop_loss(self, entry_price, current_price, stop_loss_percent=0.05):
    if current_price < entry_price * (1 - stop_loss_percent):
        return 'SELL'
    return 'HOLD'
```

### Add Take-Profit:
```python
def check_take_profit(self, entry_price, current_price, take_profit_percent=0.10):
    if current_price > entry_price * (1 + take_profit_percent):
        return 'SELL'
    return 'HOLD'
```

### Email Notifications:
```python
import smtplib
def send_email_notification(self, message):
    # Implement email notification
    pass
```

## 📊 Performance Metrics

The bot tracks:
- Total trades executed
- Win/loss ratio
- Current portfolio value
- Profit/loss (absolute and percentage)
- Trade history with timestamps

## 🤝 Contributing

Feel free to:
- Report bugs
- Suggest features
- Submit improvements
- Share your results

## ⚠️ Disclaimer

**IMPORTANT**: 
- This bot is for educational purposes
- Cryptocurrency trading involves significant risk
- Past performance does not guarantee future results
- Always test in paper mode before live trading
- Never invest more than you can afford to lose
- The authors are not responsible for financial losses

## 📄 License

Free to use for personal and educational purposes.

## 🎯 Future Enhancements

Planned features:
- Machine learning integration
- Multi-exchange support
- Advanced order types (limit, stop-loss)
- Backtesting framework
- Web dashboard
- Telegram notifications
- Portfolio diversification (multiple coins)
- News sentiment analysis

## 📞 Support

For questions or issues:
- Review this README carefully
- Check troubleshooting section
- Test in paper mode first
- Start with conservative settings

---

**Happy Trading! 🚀📈**

*Remember: The best trader is an informed trader. Study, practice, and trade responsibly.*
