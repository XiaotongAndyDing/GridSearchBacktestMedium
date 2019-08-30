import pandas as pd
import scipy.stats

import dill as dill

with open('res.pkl', 'rb') as file:
    res = dill.load(file)
df = pd.DataFrame(sorted(res, key=lambda x: x[0], reverse=True), columns=['Sharpe Ratio', 'Drawdown', 'Annual Return',
                                                                          'alpha1', 'alpha2', 'window1', 'window2',
                                                                          'multiple']).dropna()
n, euler_const, e = len(df), 0.577, 2.718
SR = df['Sharpe Ratio'].std() * (1 - euler_const) / (scipy.stats.norm.cdf(
    1 - 1 / n)) + euler_const / scipy.stats.norm.cdf(1 - 1 / (n * e))

end = None
