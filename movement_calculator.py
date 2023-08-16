import os
import datetime
import numpy as np
import pandas as pd
import yfinance as yf


def fetch_data(symbol, period, interval):
    end_date = datetime.datetime.now()
    days = int(''.join(filter(str.isdigit, period)))
    start_date = end_date - datetime.timedelta(days=days)
    file_path = f"/root/datasets/{symbol}_{period}_{interval}_data.csv"
    if not os.path.exists(file_path):
        try:
            df = yf.download(symbol, start=str(start_date.date()), end=str(end_date.date()), interval=interval)
        except ValueError as e:
            print(f"Error fetching data: {e}")
            return None
        df.reset_index(inplace=True)
        df.to_csv(file_path, index=False)
    else:
        df = pd.read_csv(file_path)
        if 'Datetime' not in df.columns:
            df = yf.download(symbol, start=str(start_date.date()), end=str(end_date.date()), interval=interval)
            df.reset_index(inplace=True)
            df.to_csv(file_path, index=False)

    try:
        if df['Datetime'].dtype != 'object':
            df['Datetime'] = df['Datetime'].astype(str)

        df['Datetime'] = df['Datetime'].str.replace(r'\+00:00$', '', regex=True)
    except ValueError as e:
        print(f"Error converting index to datetime: {e}")
        print(df)
        return None

    return df[['Datetime', 'Adj Close', 'Volume']]

def calculate_best_threshold(df, min_movement):
    percentage_changes = df['Adj Close'].pct_change()
    num_trades = []
    for threshold in np.arange(min_movement, 1, 0.0025):
        trade_mask = percentage_changes.abs() >= threshold
        num_trades.append((threshold, trade_mask.sum()))
        
    max_trade = max(num_trades, key=lambda x: x[1])
    return max_trade


def calculate_net_profit(df, threshold, fees, slippage, trading_percentage):
    percentage_changes = df['Adj Close'].pct_change()
    trade_mask = percentage_changes.abs() >= threshold

    trade_direction = percentage_changes[trade_mask].apply(np.sign)
    trade_returns = (df.loc[trade_mask, 'Adj Close'].pct_change() * trade_direction)

    # Calculate the total return by incorporating the trading_percentage with fees and slippage.
    total_return = (1 + trading_percentage * (trade_returns - trading_percentage * (fees + slippage))).product() - 1
    return total_return

def calculate_best_threshold(df, min_step=0.0001, step=0.0001, fees=0.001, slippage=0.0005, trading_percentage=1.0):
    best_score = -float('inf')
    best_threshold = 0
    best_num_trades = 0
    threshold_data = []

    for threshold in np.arange(min_step, 1, step):
        net_profit = calculate_net_profit(df, threshold, fees, slippage, trading_percentage) 

        percentage_changes = df['Adj Close'].pct_change()
        trade_mask = percentage_changes.abs() >= threshold
        num_trades = trade_mask.sum()

        # The best threshold is not only based on the percentage profit but also on the number of trades.        
        if net_profit * num_trades > 0: 
            score = np.sqrt(net_profit * num_trades)
        else:
            score = -num_trades

        threshold_data.append((threshold, num_trades, net_profit))
        
        if score > best_score:
            best_score = score
            best_threshold = threshold
            best_num_trades = num_trades

    return best_threshold, best_num_trades, threshold_data

def main():
    print('Trading Strategy Optimizer 0.1b, cbrwx.')
    user_symbol = input("Please enter the asset symbol (e.g. BTC-USD, AAPL, or MSFT): ")
    user_period = input("Please enter the period (e.g. 30d, 90d, or 180d): ")
    user_input = input("Please enter the interval (e.g. 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 1w, 1M): ")
    user_trading_percentage = input("Please enter the trading percentage (e.g. 0.1 for 10%) or press Enter for 100%: ")

    symbol = user_symbol.strip()
    period = user_period.strip()
    interval = user_input.strip()

    if user_trading_percentage.strip() == '':
        trading_percentage = 1.0
    else:
        trading_percentage = float(user_trading_percentage.strip())
    
    df = fetch_data(symbol, period, interval)

    if df is not None:
        best_threshold, best_num_trades, threshold_data = calculate_best_threshold(df)
        print(f"Best Threshold: {best_threshold * 100:.2f}%, Number of Trades: {best_num_trades}")

        # Print all non-zero thresholds, percentage profit, and the number of trades
        print("\nThresholds, Percentage Profit, and Number of Trades:")
        for threshold, num_trades, net_profit in threshold_data:
            if num_trades != 0:
                print(f"Threshold: {threshold * 100:.2f}%, Percentage Profit: {net_profit * 100:.2f}%, Number of Trades: {num_trades}")

if __name__ == "__main__":
    main()
