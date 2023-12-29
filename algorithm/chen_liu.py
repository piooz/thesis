import numpy as np
import pandas as pd
from pandas import DataFrame
import statsmodels.tsa.arima.model as tsa
import statsmodels.api as sm
import matplotlib.pyplot as plt
from arma2ma import arma2ma
from effects import combine_effects
from arma2pi import arima2poly

# def aoxa_filter(resid, picoefs):
#     n = len(resid)
#     x = np.concatenate([resid, np.zeros(n - 1)])
#     ao_xy = np.convolve(x, np.flip(picoefs), mode='valid')
#     print(ao_xy)
#     # return ao_xy
#     return np.cumsum(-1*picoefs * resid)
#

def filter_process(x, f):
    """
    works good as R recursive filter 
    """
    p = len(f)
    y = [x[0]]

    for i in range(1, len(x)):
        yi = x[i] + sum(f[j] * y[i - j - 1] for j in range(min(i, p)))
        y.append(yi)

    return y

def diff_inv(array):
    return np.r_[array[0],np.diff(array)].cumsum()

def calc_tstats(fit: tsa.ARIMAResults, residuals, sigma=None, delta=0.7):
    sigma = 1.483 * fit.mae
    IO = DataFrame(columns=['coefhat', 'tstat'])
    AO = DataFrame(columns=['coefhat', 'tstat'])
    LS = DataFrame(columns=['coefhat', 'tstat'])
    TC = DataFrame(columns=['coefhat', 'tstat'])

    ar = fit.arparams
    ma = fit.maparams
    picoefs = np.append([1], arma2ma(-ma, -ar, len(residuals)-1))

    aoxa = np.convolve(np.concatenate([ residuals, np.zeros(1) ]), np.flip(picoefs), mode='same')[1::]
    print(aoxa)
    revaoxa = aoxa[::-1]

    #IO
    IO['coefhat'] = residuals
    IO['tstat'] = residuals / sigma
    print(IO)
    #
    # AO
    xxinv = (1/np.cumsum(picoefs**2))[::-1]
    coefhat = revaoxa * xxinv
    AO['coefhat'] = coefhat
    AO['tstat'] = coefhat / (sigma * np.sqrt(xxinv))
    print(AO)
    #
    #LS
    xy = diff_inv(aoxa)
    dinvf = diff_inv(picoefs)
    xxinv = (1 / np.cumsum(dinvf**2))
    coefhat = xy * xxinv
    LS['coefhat'] = coefhat
    LS['tstat'] = coefhat / (sigma * np.sqrt(xxinv))
    print(LS)

    #TC
    # somethink is not yes
    xy = filter_process(revaoxa, [delta])[::-1]
    print(xy)
    dinvf = filter_process(picoefs, [delta])
    xxinv = (1 / np.cumsum(dinvf))[::-1]
    coefhat = xy * xxinv
    TC['coefhat'] = coefhat
    TC['tstat'] = coefhat / (sigma * np.sqrt(xxinv))
    print(TC)

    return (IO, AO, LS, TC)

def locate_outliers_inner_loop(model, residuals):
    # sigma = model.mae * 1.483
    df = calc_tstats(model, residuals)
    return df

def restructure_dataframe(df, df_hats, cval):
    # Create a new DataFrame to store the restructured data
    result_df = DataFrame()

    # Iterate over rows of the original DataFrame
    for index, row in df.iterrows():
        ind = index
        # Find the column with the maximum absolute value
        max_col = row.abs().idxmax()
        max_value = row[max_col]

        # Find the corresponding value from the second DataFrame
        coefhat = df_hats.loc[ind, max_col]

        # Append the data to the result DataFrame
        result_df = result_df._append({'ind': ind, 'type': max_col, 'tstat': max_value , 'coefhat': coefhat }, ignore_index=True)
    return DataFrame(result_df[result_df['tstat'].abs() >= cval])

def stage1(model, values, cval = 0):
    n = len(values)
    if cval == 0:
        if (n < 50):
            cval = 3
        elif (n > 450):
            cval = 4
        else:
            cval = 3 + 0.0025*(n - 50)

    for _ in range(1):
        residuals = model.resid
        residuals[0] = 0

        (IO, AO, LS, TC) = locate_outliers_inner_loop(model, residuals)
        tstat = DataFrame()
        tstat['IO'] = IO["tstat"]
        tstat['AO'] = AO["tstat"]
        tstat['LS'] = LS["tstat"]
        tstat['TC'] = TC["tstat"]
        # plt.plot(tstat)

        hat = DataFrame()
        hat['IO'] = IO["coefhat"]
        hat['AO'] = AO["coefhat"]
        hat['LS'] = LS["coefhat"]
        hat['TC'] = TC["coefhat"]

        # ingore first begging

        raport = restructure_dataframe(tstat, hat, cval)
        if raport.size != 0:
            effect = combine_effects(raport, 100, model)
            plt.plot(values)
            plt.plot(values + effect)
            model = tsa.ARIMA(DataFrame(values - effect), order=(1,0,1)).fit()

        print(raport)
    return 


def chen_liu(y):
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        y = (sm.datasets.nile.data.load_pandas().data['volume'])
        # plt.plot(y)
        model = tsa.ARIMA(y, order=(1,0,1))
        fit = model.fit()
        # plt.plot(fit.resid)
        result = stage1(fit, y, 3)
        # print(result)
        plt.plot(fit.resid)

        plt.show()
