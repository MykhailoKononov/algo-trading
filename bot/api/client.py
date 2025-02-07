import pandas as pd

from binance.client import Client
from config import config


client = Client(config.API_KEY, config.API_SECRET)


def fetch_ohlcv(symbol: str, interval: str, limit: int):
    """return full data"""
    try:
        klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
        df = pd.DataFrame(klines, columns=["timestamp", "open", "high", "low", "close", "volume",
                                           "close_time", "quote_asset_volume", "trades",
                                           "taker_base_vol", "taker_quote_vol", "ignore"])
        return df

    except Exception as e:
        print(f"Error occurred while fetching symbol: {symbol}, interval: {interval}, {e}")


def fetch_ohlcv_for_backtest(symbol: str, interval: str, limit: int):
    """return full data"""
    try:
        klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
        df = pd.DataFrame(klines, columns=[
            "timestamp", "Open", "High", "Low", "Close", "Volume",
            "Close_time", "Quote_asset_volume", "Number_of_trades",
            "Taker_buy_base_vol", "Taker_buy_quote_vol", "Ignore"
        ])

        df = df.astype({
            "Open": "float64",
            "High": "float64",
            "Low": "float64",
            "Close": "float64",
            "Volume": "float64"
        })

        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df.set_index("timestamp", inplace=True)

        df = df[["Open", "High", "Low", "Close", "Volume"]]


        return df

    except Exception as e:
        print(f"Error occurred while fetching symbol: {symbol}, interval: {interval}, {e}")
