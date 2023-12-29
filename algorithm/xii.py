import numpy as np
import statsmodels
import pandas as pd
from pandas import DataFrame, Series
import statsmodels.tsa.arima.model as tsa
import statsmodels.api as sm
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_process import arma_impulse_response
from scipy.signal import lfilter
from arma2ma import arma2ma


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

def calcxx(residuals:Series, model, delta:float ):
    df = DataFrame()
    df["residuals"] = residuals

    ar = model.arparams
    ma = model.maparams
    print(ar,ma)

    n = len(residuals)

    # pi = arma2ma(ar, ma, len(residuals))
    pi = np.append([1], arma2ma(-ma, -ar, n-1))
    print(f"pi coefs\n {pi}")

    # calc x1x2
    df["IO"] = np.zeros(n)

    df["AO"] = -pi

    # calc x3
    x2 = np.zeros_like(pi, dtype=float);
    for t in range(n):
        x2[t] = 1 - np.sum(pi[:t])
    df["LS"] = x2


    # calc x4
    x4 = np.zeros_like(pi, dtype=float)
    max_delta = delta**n
    for t in range(n):
        x4[t] = max_delta - np.sum(pi[:min(t+1, n)]) - pi[min(t, n-1)]

    df['TC'] = x4

    return df

def calculate_omega(x, residuals):
    output = np.zeros(len(x))
    for t in range(len(x)):
        numerator = np.sum(residuals[t:] * x[t:])
        denominator = np.sum(x[t:]**2)

        if denominator != 0:
            output[t] = numerator / denominator
        else:
            output[t] = 0

    return output

def calculate_tau(omega, x, sigma):
    n = len(x)
    tau = np.zeros(n)  # Initialize an array to store tau values

    for t in range(n):
        # Calculate the summation of squared values of x from t1 to n
        summation = np.sum(x[t:]**2)

        # Calculate the tau value using the given formula
        tau[t] = (omega[t] / sigma) * summation

    return tau

def calc_aoxy(fit):
    """
    Works good
    """
    ar = fit.arparams
    ma = fit.maparams

    pi = np.append([1], arma2ma(-ma, -ar, len(fit.resid)-1))

    n = len(fit.resid)
    zero_padding = np.zeros(n - 1)

    # Concatenate 'resid' and zero-padding
    x = np.concatenate((fit.resid, zero_padding))

    # Reverse the 'picoefs'
    picoefs_reversed = np.flip(pi)

    # Perform convolution
    ao_xy = np.convolve(x, picoefs_reversed, mode='valid')

    print("aoxy\n", ao_xy)
    xxinv = np.flip(1/np.cumsum(pi**2))
    print("xxinv\n", xxinv)
    return ao_xy, xxinv


def diff_inv(array):
    inverted_diff = np.cumsum(np.append([0],(array)))
    return inverted_diff


def tstat(fit, data):
    sigma = 1.483 * fit.mae
    df = DataFrame()

    # df['IOcoef']  = fit.resid
    # df['IOtstat'] = fit.resid / sigma
    #
    # # xiinv = (1/data["AO"]**2)[::-1]
    # # aoxo = (fit.resid*data["AO"]).cumsum()[::-1]
    #
    # coef = aoxo * xiinv

    # coef = calculate_omega(data['AO'], fit.resid )

    aoxy, xxinv = calc_aoxy(fit)
    coef2 = aoxy * xxinv
    tstat2 = coef2 / (sigma * np.sqrt(xxinv))
    df['AOcoef'] = coef2
    df['AOtstat'] = tstat2


    # coef3 = calculate_omega(data['LS'], fit.resid )
    # tstat3 = calculate_tau(coef3, data['LS'], sigma)

    ar = fit.arparams
    ma = fit.maparams
    pi = np.append([1], arma2ma(-ma, -ar, len(fit.resid)-1))

    aoxy_rev = np.flip(aoxy)

    xy = np.flip(diff_inv(aoxy_rev)[1::])
    dinvf = diff_inv(pi)[1::]
    xxinv3 = np.flip(1/np.cumsum(dinvf**2))

    coef3 = xy * xxinv3
    tstat3 = coef3 / (sigma * np.sqrt(xxinv3))


    df['LScoef'] = coef3
    df['LStstat'] = tstat3

    coef4 = calculate_omega(data['TC'], fit.resid )
    tstat4 = calculate_tau(coef4, data['TC'], sigma)


    xy = np.flip(filter_process(aoxy_rev, [0.7]))
    dinvf = filter_process(pi, [0.7])
    print(xy)
    print(dinvf)
    xxinv4 = np.flip(1/ np.cumsum(dinvf**2))
    coef4 = xy * xxinv4
    tstat4 = coef4 / (sigma * np.sqrt(xxinv4))

    df['TCcoef'] = coef4
    df['TCtstat'] = tstat4

    print(df)
    return df




if __name__ == "__main__":
    with pd.option_context('display.max_rows', None, 'display.max_columns', None, ):
        y = sm.datasets.get_rdataset('Nile').raw_data['value']
        df = DataFrame(y)
        model = tsa.ARIMA(y, order=(1,0,1))
        fit = model.fit()
        output = calcxx(fit.resid, fit, 0.7)
        dupa = tstat(fit,output)
        plt.plot(dupa['AOtstat'])
        plt.plot(dupa['LStstat'])
        plt.plot(dupa['TCtstat'])
        plt.show()
