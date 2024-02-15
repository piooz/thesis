import numpy as np
from pandas import DataFrame, Series, pandas
import statsmodels.tsa.arima.model as tsa
from . import arma2ma
from .logger import logging


def ao_effect(n, ind, w=1):
    array = np.zeros(n)
    array[ind] = w
    return array


def tc_effect(n, ind, w=1, delta=0.7):
    # logging.debug(f'w: {w}')
    result = np.zeros(n)
    for i in range(0, n - ind):
        result[i + ind] = (delta**i) * w
    return result


def ls_effect(n, ind, w=1):
    result = np.zeros(n)
    for i in range(ind, n):
        result[i] = 1
    return result * w


def io_effect(n, ind, ar, ma, w=1):
    arr = arma2ma(ar, ma, n - ind - 1)
    arr = np.concatenate([np.zeros(ind), [1], arr])
    return arr * w


def sls_effect(n, ind, freq, w=1):
    result = np.zeros(n)
    for i in range(0, n - ind):
        if i % freq == 0:
            result[ind + i] = 1
    return result * w


def parse_row(row: Series, n: int, delta, model: tsa.ARIMAResults):
    ind = row['ind']
    w = row['coefhat']
    # logging.debug(f'{row}')
    ar = [1]
    ma = [1]

    ar = model.arparams
    ma = model.maparams

    match row['type']:
        case 'TC':
            effect = tc_effect(n, ind, w, delta)
            # logging.debug(f'coefhat: {w} effect TC: {effect} ')
            return effect
        case 'IO':
            effect = io_effect(n, ind, ar, ma, w)
            # logging.debug(f'coefhat: {w} effect IO: {effect} ')
            return effect
        case 'AO':
            effect = ao_effect(n, ind, w)
            # logging.debug(f'coefhat: {w} effect AO: {effect} ')
            return effect
        case 'LS':
            effect = ls_effect(n, ind, w)
            # logging.debug(f'coefhat: {w} effect LS: {effect} ')
            return effect
        case _:
            return 0


def combine_effects(
    data, n, fit: tsa.ARIMAResults | None = None, freq=12, delta=0.7
):

    # logging.debug(f'input: {data}')
    result = np.zeros(n)
    for _, row in data.iterrows():
        arr = parse_row(row, n, delta, fit)
        result += arr
    # logging.debug(f'result: {result}')
    return result


def get_dataframe_effects(
    data, n, fit: tsa.ARIMAResults | None = None, freq=12, delta=0.7
):
    di = {}

    for i, row in data.iterrows():
        row['coefhat'] = 1
        arr = parse_row(row, n, delta, fit)
        colname = f'{row["type"]}_{i}'
        di[colname] = arr
        # df = pandas.concat([df, DataFrame(arr, columns=[colname])])

    df = DataFrame(di)

    return df


if __name__ == '__main__':
    pass
