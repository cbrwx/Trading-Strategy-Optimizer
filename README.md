# Trading-Strategy-Optimizer
This simple tool fetches historical price data using the Yahoo Finance library, calculates the best threshold for triggering trades, and evaluates the potential profitability of different threshold levels.
## Features
- Fetches historical price data for a specified asset using Yahoo Finance.
- Calculates the best threshold value for triggering buy or sell trades.
- Evaluates the potential net profitability of the trading strategy.
- Considers trading fees, slippage, and a user-defined trading percentage.
- Outputs the best threshold percentage and corresponding number of trades.
- Displays a list of different threshold values along with their profitability and trade counts.

## Installation

- Clone or download the repository to your local machine.
- Install the required Python packages by running:
```
pip install numpy pandas yfinance
```

## Usage

- Run the script by executing python trading_strategy_optimizer.py.
- Follow the prompts to input the asset symbol, period, interval, and trading percentage (optional).
- The script will fetch historical price data, calculate the best threshold, and display the results.

Example output:
```
Trading Strategy Optimizer 0.1b, cbrwx.
Please enter the asset symbol (e.g. BTC-USD, AAPL, or MSFT): AAPL
Please enter the period (e.g. 30d, 90d, or 180d): 90d
Please enter the interval (e.g. 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 1w, 1M): 1d
Please enter the trading percentage (e.g. 0.1 for 10%) or press Enter for 100%: 0.1
Best Threshold: 0.55%, Number of Trades: 38

Thresholds, Percentage Profit, and Number of Trades:
Threshold: 0.10%, Percentage Profit: 9.73%, Number of Trades: 46
Threshold: 0.15%, Percentage Profit: 4.16%, Number of Trades: 45
Threshold: 0.20%, Percentage Profit: 3.14%, Number of Trades: 44
...
```

To make the code work on your system, you should adjust the file_path to a directory that you have access to and prefer for storing the data. For example:

```
file_path = f"your/preferred/directory/{symbol}_{period}_{interval}_data.csv"
```

.cbrwx
