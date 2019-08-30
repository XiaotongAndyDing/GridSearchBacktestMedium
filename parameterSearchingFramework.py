import dill as dill

from momentumStrategyWithVolatilityVolumeFilter import strategy
import itertools

res = []
for alpha1, alpha2, window1, window2, multiple in itertools.product([0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
                                                                    [0.001, 0.005, 0.01, 0.02, 0.03, 0.05, 0.1, 0.2,
                                                                     0.3],
                                                                    [3, 5, 10, 20], [10, 20, 30, 50, 100],
                                                                    [0.8, 0.9, 1, 1.1, 1.2, 1.3]):
    if alpha1 > alpha2 and window1 < window2:
        sharpe_ratio, max_drawdown, annual_return = strategy(alpha1, alpha2, window1, window2, multiple)
        res.append(
            (sharpe_ratio, max_drawdown, annual_return, alpha1, alpha2, window1, window2, multiple))

with open('res.pkl', 'wb') as file:
    dill.dump(res, file)
