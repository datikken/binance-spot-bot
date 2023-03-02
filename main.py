from binance.client import Client
from dotenv import load_dotenv
import pandas as pd
import os
import time


load_dotenv()


api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')

client = Client(api_key, api_secret)


def top_coin():
    all_tickers = pd.DataFrame(client.get_ticker())
    usdt = all_tickers[all_tickers.symbol.str.contains('USDT')]
    work = usdt[~((usdt.symbol.str.contains('UP')) |
                  (usdt.symbol.str.contains('DOWN')))]
    top_coin = work[work.priceChangePercent == work.priceChangePercent.max()]
    top_coin = top_coin.symbol.values[0]
    return top_coin


def last_data(symbol, interval, lookback):
    frame = pd.DataFrame(client.get_historical_klines(
        symbol, interval, lookback + 'min ago UTC'))
    frame = frame.iloc[:, :6]
    frame.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    frame = frame.set_index('Time')
    frame.index = pd.to_datetime(frame.index, unit='ms')
    frame = frame.astype(float)
    return frame


def strategy(buy_amt, SL=0.985, Target=1.02, open_position=False):
    try:
        asset = top_coin()
        df = last_data(asset, '1m', '120')
    except:
        time.sleep(61)
        asset = top_coin()
        df = last_data(asset, '1m', '120')

    print(asset)

    qty = round(buy_amt / df.Close.iloc[-1], 1)

    if ((df.Close.pct_change() + 1).cumprod()).iloc[-1] > 1:
        print('===')
        print(asset)
        print(df.Close.iloc[-1])
        print(qty)
        print('===')

        order = client.create_order(
            symbol=asset, side='BUY', type='MARKET', quantity=qty)
        print(order)

        buyprice = float(order['fills'][0]['price'])
        open_position = True

        while open_position:
            try:
                df = last_data(asset, '1m', '2')
            except:
                print('Restarting')
                time.sleep(61)
                df = last_data(asset, '1m', '2')

            print(f'Price {str(df.Close[-1])}')
            print(f'Target {str(buyprice * Target)}')
            print(f'Stop {str(buyprice * SL)}')

            if df.Close[-1] <= buyprice * SL or df.Close[-1] >= buyprice * Target:
                order = client.create_order(
                    symbol=asset, side='SELL', type='MARKET', quantity=qty)
                print('SELLING: ', order)
                break
    else:
        print('No clue')
        time.sleep(20)


while True:
    strategy(15)
