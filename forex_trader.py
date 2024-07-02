import json
import yfinance as yf
import requests
from collections import deque
import time
import base64
import hashlib
import hmac
from datetime import datetime


api_key = "YOUR_API_KEY"
secret_key = "YOUR_SECRET_KEY"
account_id = "YOUR_ACCOUNT_ID"
api_url = "SCHWAB URL" 


def generate_headers():
    timestamp = str(int(datetime.now().timestamp() * 1000))
    message = api_key + timestamp
    signature = base64.b64encode(hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).digest()).decode()
    
    return {
        "X-API-Key": api_key,
        "X-Timestamp": timestamp,
        "X-Signature": signature,
        "Content-Type": "application/json"
    }


def main():
    ticker = "EURUSD=X"
    interval = "5m"
    period = "1mo"

    while True:
        try:
            priceData = yf.download(tickers=ticker, interval=interval, period=period)

            prices_close = deque(priceData['Close'].tail(15), maxlen=15)
            prices_high = deque(priceData['High'].tail(15), maxlen=15)
            prices_low = deque(priceData['Low'].tail(15), maxlen=15)
            prices_open = deque(priceData['Open'].tail(15), maxlen=15)

            get_signal(prices_close, prices_open)

            time.sleep(300)

        except KeyboardInterrupt:
            print("Ending trading session")
            break  


def get_signal(prices_close, prices_open):

    pips_per_candleLONG = calculate_pips_per_candle_LONG(prices_open, prices_close, pip_size=0.0001)
    pips_per_candleSHORT = calculate_pips_per_candle_SHORT(prices_open, prices_close, pip_size=0.0001)


    for pips, signalLONG in enumerate(pips_per_candleLONG,start=1):
        print(f"{pips}: Long Signal: {signalLONG}")


    for pips, signalShort in enumerate(pips_per_candleSHORT,start=1):
        print(f"{pips}: Short Signal: {signalShort}")


def calculate_pips_per_candle_LONG(prices_open, prices_close, pip_size=0.0001):

    pips_per_candle = []
    longSignal = False

    for open_price, close_price in zip(prices_open, prices_close):
        pip_difference = (close_price - open_price) / pip_size
        pips_per_candle.append(pip_difference)

        for i in range(len(pips_per_candle) - 2):
            if abs(pips_per_candle[i]) >= 3.2 and abs(pips_per_candle[i+1]) >= 3.2 and abs(pips_per_candle[i+2]) >= 3.2:
                longSignal = True
                #buy_long()
                break

    return pips_per_candle, longSignal


def calculate_pips_per_candle_SHORT(prices_open, prices_close, pip_size=0.0001):

    pips_per_candle = []
    shortSignal = False

    for open_price, close_price in zip(prices_open, prices_close):
        pip_difference = (close_price - open_price) / pip_size
        pips_per_candle.append(pip_difference)

        for i in range(len(pips_per_candle) - 2):
            if abs(pips_per_candle[i]) <= -3.2 and abs(pips_per_candle[i+1]) <= -3.2 and abs(pips_per_candle[i+2]) <= -3.2:
                shortSignal = True
                #buy_short()
                break

    return pips_per_candle, shortSignal



def stop_loss_long():

    time.sleep(3600)

def take_profit_long():

    time.sleep(3600)

def stop_loss_short():

    time.sleep(3600)

def take_profit_short():

    time.sleep(3600)



def buy_long():

    ticker = "EURUSD=X"
    account_id = " "

    order_data = {
        "accountId": account_id,
        "symbol": ticker,
        "quantity": 50000,
        "orderType": "MARKET",
        "action": "BUY",
        "timeInForce": "GTC"
    }

    headers = generate_headers()
    response = requests.post(f"{api_url}/orders", headers=headers, data=json.dumps(order_data))

    if response.status_code == 200:
        print("Buy order submitted successfully")
        print(response.json())
    else:
        print(f"Error submitting buy order: {response.status_code}")
        print(response.text)


def buy_short():

    ticker = "EURUSD=X"
    account_id = " "

    order_data = {
        "accountId": account_id,
        "symbol": ticker,
        "quantity": 50000,
        "orderType": "MARKET",
        "action": "SELL",
        "timeInForce": "GTC"
    }

    headers = generate_headers()
    response = requests.post(f"{api_url}/orders", headers=headers, data=json.dumps(order_data))

    if response.status_code == 200:
        print("Sell order submitted successfully")
        print(response.json())
    else:
        print(f"Error submitting buy order: {response.status_code}")
        print(response.text)


if __name__ == "__main__":
    main()