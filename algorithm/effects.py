import numpy as np
import statsmodels
from pandas import DataFrame, Series
import statsmodels.tsa.arima.model as tsa
import statsmodels.api as sm
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_process import arma_impulse_response
from scipy.signal import lfilter
from arma2ma import arma2ma


def ao_effect(n, ind, w=1):
    array = np.zeros(n)
    array[ind] = w
    return array

def tc_effect(n, ind, w=1, delta=0.7):
    result = np.zeros(n)
    for i in range(0, n-ind):
        result[i+ind] = (delta**i)*w
    return result

def ls_effect(n, ind, w=1):
    result = np.zeros(n)
    for i in range(ind, n):
        result[i] = 1
    return result * w

def io_effect(n, ind, ar, ma, w=1):
    arr = arma2ma(ar, ma, n-ind)
    print(arr)
    arr = arr / arr.max()
    arr = np.concatenate([np.zeros(ind), arr])
    return arr * -w

def sls_effect(n, ind, freq, w=1):
    result = np.zeros(n)
    for i in range(0, n-ind):
        if i % freq == 0:
            result[ind+i] = 1
    return result * w


def parse_row(row:Series, n:int, delta, model:tsa.ARIMAResults):
    ind = row['ind']
    w = row['coefhat']
    ar = [1]
    ma = [1]

    ar = model.arparams
    ma = model.maparams


    match row['type']:
        case 'TC':
            return tc_effect(n, ind, w, delta)
        case 'IO':
            return io_effect(n, ind, ar, ma, w)
        case 'AO':
            return ao_effect(n,ind,w)
        case 'LS':
            return ls_effect(n,ind,w)
        case _:
            return 0


def combine_effects(data:DataFrame, n, model:tsa.ARIMAResults|None = None, freq=12, delta=0.7):
    if data.size == 0:
        return
    data['to'] = np.roll(data['ind'],-1)
    data['to'].iat[-1] = n
    print(data['to'])

    result = np.array([])
    for _, row in data.iterrows():
        arr = parse_row(row, n, delta, model)
        arr = arr[row['ind']:row['to']:]
        result = np.append(result, arr)
    result = np.append(np.zeros(n - len(result)), result)
    print(f"dupa {len(result)}")
    print(result)
    return result


if __name__ == "__main__":
    y = (sm.datasets.nile.data.load_pandas().data['volume'])
    # plt.plot(y)
    model = tsa.ARIMA(y, order=(1,0,1))
    fit = model.fit()
    ar = fit.arparams
    ma = fit.maparams
    out = io_effect(100,10,ar,ma,-390)
    plt.plot(out);
    # plt.plot(abs(arma2ma(ar,ma,100)))
    # plt.plot(arma2ma([0.8610783],[-0.5176954],10))
    plt.show();
