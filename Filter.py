import numpy as np


class RollingMeanFilter(object):

    def __init__(self, window1, window2, multiple, df):
        assert window1 < window2
        self.rolling_mean1 = df.rolling(window=window1).mean()
        self.rolling_mean2 = df.rolling(window=window2).mean()
        self.ratio = self.rolling_mean1 / self.rolling_mean2
        self.filter = self.rolling_mean1 > multiple * self.rolling_mean2


class RollingStdFilter(object):

    def __init__(self, window1, window2, multiple, df):
        assert window1 < window2
        self.rolling_std1 = df.rolling(window=window1).std() / np.sqrt(window1)
        self.rolling_std2 = df.rolling(window=window2).std() / np.sqrt(window2)
        self.ratio = self.rolling_std1 / self.rolling_std2
        self.filter = self.rolling_std1 > multiple * self.rolling_std2

