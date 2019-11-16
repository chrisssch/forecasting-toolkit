__author__ = "Christoph Schauer"
__date__ = "2019-11-13"
__version__ = "0.2"


import numpy
from pandas import Series, period_range
from sklearn.linear_model import LinearRegression


class LinearTrend(LinearRegression):
    """
    Child class of sklearn.linear_model.LinearRegression, inheriting everything from this
    class. Extends this class with several attributes and methods for easy-to-use modeling and
    forecasting of time series with linear and polynomial regression models.
    Requires as input and returns as output pandas series with PeriodIndex.
    """
    def __init__(
        self, y, polynomials=1,
        fit_intercept=True, normalize=False, copy_X=True, n_jobs=None
        ):
        super().__init__(fit_intercept, normalize, copy_X, n_jobs)

        self.y = y
        self.polynomials = polynomials
        self.X_endog = None


    def gen_X_endog(self, start, stop):
        """
        Generates an array with a time sequence as input for the 'fit_ts' method.
        """
        X_endog = numpy.arange(start, stop).reshape(-1, 1)
        for p in range(2, self.polynomials + 1):
            x_endog_p = (numpy.arange(start, stop)**p).reshape(-1, 1)
            X_endog = numpy.concatenate([X_endog, x_endog_p], axis=1)
        return X_endog


    def fit_ts(self):
        """
        Fits a linear regression model with features generated by the 'gen_X_endog' method to
        'self.y'.
        """
        self.X_endog = self.gen_X_endog(start=0, stop=len(self.y.index))
        self.fit(self.X_endog, self.y)
        return self


    def predict_ts(self):
        """
        Predicts values for 'self.y' with the fitted model.
        """
        y_pred = self.predict(self.X_endog)
        return Series(y_pred, index=self.y.index)


    def forecast_ts(self, steps):
        """
        Forecasts values for 'steps' steps after the last period in 'self.y.index'.
        """
        idx_fcst = period_range(self.y.index[-1] + 1, periods=steps)
        X_endog = self.gen_X_endog(start=len(self.y), stop=len(self.y) + steps)
        y_fcst = self.predict(X_endog)
        return Series(y_fcst, index=idx_fcst)
