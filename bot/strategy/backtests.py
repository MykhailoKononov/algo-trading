from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA
import talib


class SMAStrategy(Strategy):
    fast_ma_period = 0
    slow_ma_period = 0

    def init(self):
        """
        Метод инициализации. Здесь мы рассчитываем индикаторы,
        используя встроенную функцию I(), чтобы индикаторы пересчитывались автоматически.
        """
        self.fast_ma = self.I(talib.SMA, self.data.Close, self.fast_ma_period)
        self.slow_ma = self.I(talib.SMA, self.data.Close, self.slow_ma_period)

    def next(self):
        """
        Метод, вызываемый на каждом новом баре.
        Если быстрая скользящая средняя выше медленной и позиции нет.
        Если быстрая скользящая средняя ниже медленной и позиция открыта.
        """
        # Если сигнал на покупку и позиции ещё нет
        if crossover(self.slow_ma, self.fast_ma) and not self.position:
            self.buy()
        # Если сигнал на продажу и позиция открыта – закрываем её
        elif crossover(self.fast_ma, self.slow_ma) and self.position:
            self.position.close()
            self.sell()
