from backtesting import Strategy
from backtesting.lib import crossover
from talib import EMA, SMA


class MaCrossover(Strategy):
    """
    Стратегия пересечения скользящих средних.
    """

    ma_short_timeperiod = 50
    ma_long_timeperiod = 200
    ma_short_type = "SMA"
    ma_long_type = "SMA"

    def init(self):
        # Словарь функций скользящих средних
        ma_funcs = {"SMA": SMA, "EMA": EMA}

        # Валидация типов MA
        if self.ma_short_type not in ma_funcs:
            raise ValueError(f"Неизвестный тип короткой MA: {self.ma_short_type}")
        if self.ma_long_type not in ma_funcs:
            raise ValueError(f"Неизвестный тип длинной MA: {self.ma_long_type}")

        # Создание индикаторов
        self.ma_short = self.I(
            ma_funcs[self.ma_short_type],
            self.data.Close,
            self.ma_short_timeperiod,
            name=f"{self.ma_short_type}_{self.ma_short_timeperiod}",
        )

        self.ma_long = self.I(
            ma_funcs[self.ma_long_type],
            self.data.Close,
            self.ma_long_timeperiod,
            name=f"{self.ma_long_type}_{self.ma_long_timeperiod}",
        )

    def next(self):
        # Длинная позиция при пересечении снизу вверх
        if crossover(self.ma_short, self.ma_long):
            self.position.close()
            self.buy()

        # Короткая позиция при пересечении сверху вниз
        elif crossover(self.ma_long, self.ma_short):
            self.position.close()
            self.sell()
