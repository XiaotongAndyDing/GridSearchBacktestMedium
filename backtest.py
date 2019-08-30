import dill
import pandas as pd
import pandas_datareader.data as web


class SP500Backtest(object):

    def __init__(self):
        try:
            with open('SP500.pkl', 'rb') as file:
                self.df = dill.load(file)
        except FileNotFoundError:
            self.df = web.DataReader('^GSPC', 'yahoo', start='2010-01-01', end='2018-08-01')
            with open('SP500.pkl', 'wb') as file:
                dill.dump(self.df, file)
        self.annual_return = None
        self.annualized_sharpe_ratio = None
        self.drawdown = None

    def mini_backtest(self, long, short):
        money, inv_rate = 1, 1
        book = [(self.df.index[0], money)]
        for idx, val in enumerate(self.df.index[1:-2]):
            """we assume re-balance every day"""
            if long[val]:
                money = (1 - inv_rate) * money + inv_rate * money * (
                        self.df['Close'][self.df.index[idx + 2]] / self.df['Close'][self.df.index[idx + 1]])
            elif short[val]:
                money = (1 - inv_rate) * money + inv_rate * money * (
                        self.df['Close'][self.df.index[idx + 1]] / self.df['Close'][self.df.index[idx + 2]])
            book.append((val, money))
        backtest = pd.DataFrame(book, columns=['datetime', 'port_val'])
        backtest.set_index(['datetime'], inplace=True)
        backtest_daily_return = backtest.pct_change(1)

        self.annual_return = backtest.iloc[-1] ** (365 / len(backtest)) - 1
        self.annualized_sharpe_ratio = self.annual_return / (backtest_daily_return.std() * (365 ** 0.5))
        self.drawdown = max(((backtest.cummax() - backtest) / backtest.cummax())['port_val'])
