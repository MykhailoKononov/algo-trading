from backtesting import Backtest
from bot.strategy.backtests import SMAStrategy
from bot.api.client import fetch_ohlcv_for_backtest, fetch_ohlcv

if __name__ == "__main__":
    df = fetch_ohlcv_for_backtest("PEPEUSDT", interval="15m", limit=5000)
    bt = Backtest(df, SMAStrategy, cash=10000, commission=0.002)
    stats = bt.optimize(
        fast_ma_period=range(5, 40, 5),
        slow_ma_period=range(20, 80, 5),
        stop_loss_pct=[0.01, 0.02, 0.03, 0.04, 0.05],
        take_profit_pct=[0.02, 0.04, 0.06, 0.08],
        maximize="Return [%]",
        constraint=lambda param: param.fast_ma_period < param.slow_ma_period
    )

    best_params = stats._strategy.__dict__
    best_fast_ma = best_params["fast_ma_period"]
    best_slow_ma = best_params["slow_ma_period"]
    best_stop_loss_pct = best_params["stop_loss_pct"]
    best_take_profit_pct = best_params["take_profit_pct"]

    print(f"Best params: fma={best_fast_ma}, sma={best_slow_ma}, tp={best_take_profit_pct}, sl={best_stop_loss_pct}")

    bt_best = Backtest(df, SMAStrategy, cash=10000, commission=0.002)
    print(bt_best.run(
        fast_ma_period=best_fast_ma,
        slow_ma_period=best_slow_ma,
        stop_loss_pct=best_stop_loss_pct,
        take_profit_pct=best_take_profit_pct)
    )
    bt_best.plot()
