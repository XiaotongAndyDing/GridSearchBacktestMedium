import pandas as pd
from EMA import EMA
from Filter import RollingStdFilter, RollingMeanFilter
from backtest import SP500Backtest


def strategy(alpha1, alpha2, window1, window2, multiple):
    d = SP500Backtest()
    s_long = EMA(alpha1, alpha2, d.df)
    s_short = EMA(alpha1, alpha2, d.df)
    vol_filter = RollingStdFilter(window1, window2, multiple, d.df.Close).filter
    volume_filter = RollingMeanFilter(window1, window2, multiple, d.df.Volume).filter
    filter_all = volume_filter & vol_filter

    long_signal = [False]
    for val in s_long.long.index[1:]:
        if long_signal[-1] and s_long.long[val]:
            long_signal.append(True)
        elif not long_signal[-1] and s_long.long[val] and filter_all[val]:
            long_signal.append(True)
        else:
            long_signal.append(False)
    long_signal = pd.Series(long_signal, index=s_long.long.index)

    short_signal = [False]
    for val in s_short.short.index[1:]:
        if short_signal[-1] and s_short.short[val]:
            short_signal.append(True)
        elif not short_signal[-1] and s_short.short[val] and filter_all[val]:
            short_signal.append(True)
        else:
            short_signal.append(False)
    short_signal = pd.Series(short_signal, index=s_short.short.index)

    d.mini_backtest(long_signal, short_signal)
    return float(d.annualized_sharpe_ratio), float(d.drawdown), float(d.annual_return)
