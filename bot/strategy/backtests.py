from backtesting import Strategy
from backtesting.lib import crossover
import talib


class SMAStrategy(Strategy):
    fast_ma_period = 10
    slow_ma_period = 30
    stop_loss_pct = 0.02  # 2% стоп-лосс
    take_profit_pct = 0.04  # 4% тейк-профит

    def init(self):
        self.fast_ma = self.I(talib.SMA, self.data.Close, self.fast_ma_period)
        self.slow_ma = self.I(talib.SMA, self.data.Close, self.slow_ma_period)

    def next(self):
        price = self.data.Close[-1]

        # Открываем сделку при пересечении вверх
        if crossover(self.fast_ma, self.slow_ma) and not self.position:
            self.buy(sl=price * (1 - self.stop_loss_pct), tp=price * (1 + self.take_profit_pct))

        # Закрываем сделку при пересечении вниз
        elif crossover(self.slow_ma, self.fast_ma) and self.position:
            self.position.close()