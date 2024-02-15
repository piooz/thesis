import numpy as np
import pandas as pd
from pandas import DataFrame
import statsmodels.tsa.arima.model as tsa
import statsmodels.api as sm
from .arma2ma import arma2ma
from .logger import logging


def diff_inv(array):
    inverted_diff = np.cumsum(np.append([0], (array)))
    return inverted_diff


def filter_process(x, f):
    """
    works good as R recursive filter
    """
    p = len(f)
    y = [x[0]]

    for i in range(1, len(x)):
        yi = x[i] + sum(f[j] * y[i - j - 1] for j in range(min(i, p)))
        y.append(yi)

    return np.array(y)


def _calc_aoxy(fit, pi):
    """
    Calculate statics for tstat function (probobly you wouldn't need that)
    """
    n = len(fit.resid)
    zero_padding = np.zeros(n - 1)

    x = np.concatenate((fit.resid, zero_padding))
    picoefs_reversed = np.flip(pi)
    ao_xy = np.convolve(x, picoefs_reversed, mode='valid')

    # logging.debug(f'aoxy\n{ao_xy}')
    xxinv = np.flip(1 / np.cumsum(pi**2))
    # logging.debug(f'xxinv\n{xxinv}')
    return ao_xy, xxinv


def tstat(fit):
    sigma = 1.483 * fit.mae

    ar = fit.arparams
    ma = fit.maparams
    pi = np.append([1], arma2ma(-ma, -ar, len(fit.resid) - 1))

    aoxy, xxinv = _calc_aoxy(fit, pi)
    aoxy_rev = np.flip(aoxy)

    df = DataFrame()

    df['IOcoef'] = fit.resid
    df['IOtstat'] = fit.resid / sigma

    coef2 = aoxy * xxinv
    tstat2 = coef2 / (sigma * np.sqrt(xxinv))
    df['AOcoef'] = coef2
    df['AOtstat'] = tstat2

    xy = np.flip(diff_inv(aoxy_rev)[1::])
    dinvf = diff_inv(pi)[1::]
    xxinv3 = np.flip(1 / np.cumsum(dinvf**2))

    coef3 = xy * xxinv3
    tstat3 = coef3 / (sigma * np.sqrt(xxinv3))

    df['LScoef'] = coef3
    df['LStstat'] = tstat3

    xy = np.flip(filter_process(aoxy_rev, [0.7]))
    dinvf = filter_process(pi, [0.7])
    # logging.debug(xy)
    # logging.debug(dinvf)
    xxinv4 = np.flip(1 / np.cumsum(dinvf**2))
    coef4 = xy * xxinv4
    tstat4 = coef4 / (sigma * np.sqrt(xxinv4))

    df['TCcoef'] = coef4
    df['TCtstat'] = tstat4

    # logging.debug(df)
    return df


if __name__ == '__main__':
    pass
