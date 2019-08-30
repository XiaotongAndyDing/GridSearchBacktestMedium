class EMA(object):

    def __init__(self, alpha1, alpha2, df_day):
        self.rolling_mean1 = df_day.Close.ewm(alpha=alpha1).mean()
        self.rolling_mean2 = df_day.Close.ewm(alpha=alpha2).mean()
        self.long = self.rolling_mean1 > self.rolling_mean2
        self.short = self.rolling_mean1 < self.rolling_mean2
