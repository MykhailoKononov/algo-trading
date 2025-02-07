from backtesting import Backtest
from bot.strategy.backtests import SMAStrategy
from bot.api.client import fetch_ohlcv_for_backtest, fetch_ohlcv

if __name__ == "__main__":
    df = fetch_ohlcv_for_backtest("PEPEUSDT", interval="15m", limit=1000)
    bt = Backtest(df, SMAStrategy, cash=10000, commission=0.002)
    stats = bt.optimize(fast_ma_period=range(5, 50, 5),
                        slow_ma_period=range(20, 100, 5),
                        maximize="Return [%]",
                        constraint=lambda param: param.fast_ma_period < param.slow_ma_period)
    best_params = stats._strategy.__dict__
    best_fast_ma = best_params["fast_ma_period"]
    best_slow_ma = best_params["slow_ma_period"]

    print(f"Best params: fast_ma_period={best_fast_ma}, slow_ma_period={best_slow_ma}")

    bt_best = Backtest(df, SMAStrategy, cash=10000, commission=0.002)
    print(bt_best.run(fast_ma_period=best_fast_ma, slow_ma_period=best_slow_ma))
    bt_best.plot()
