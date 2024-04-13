import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import statsmodels.tsa.arima.model as tsa
from .effects import combine_effects, get_dataframe_effects
from . import xii
import re
from .logger import logging


def calc_cval(n):
    cval = 3
    if cval == 0:
        if n < 50:
            cval = 3
        elif n > 450:
            cval = 4
        else:
            cval = 3 + 0.0025 * (n - 50)
    return cval


def extract_values(row, cval=3):
    types = ['IO', 'AO', 'LS', 'TC']
    t_values = [row[f'{type}tstat'] for type in types]

    valid_types = [
        types[i] for i in range(len(types)) if abs(t_values[i]) > cval
    ]

    if not valid_types:
        return Series({'type': None, 'coefhat': None, 'tstat': None})

    max_type = max(valid_types, key=lambda t: abs(row[f'{t}tstat']))

    return Series(
        {
            'type': max_type,
            'coefhat': row[f'{max_type}coef'],
            'tstat': row[f'{max_type}tstat'],
        }
    )


def locate_outliers_inner_loop(fit, cval, result):
    stats = xii.tstat(fit)
    outliers = stats.apply(extract_values, cval=cval, axis=1)
    outliers = outliers.dropna()
    logging.debug(stats)
    if result is not None:
        result += outliers
    return (outliers, stats)


def stage1(
    fit: tsa.ARIMAResults,
    values,
    cval: float = 0.0,
    arima_order: tuple = (1, 0, 1),
):
    n = len(values)
    if cval == 0:
        cval = calc_cval(n)

    result = None
    effect = None
    values_copy = values.copy()
    stats = None
    for _ in range(2):

        result, stats = locate_outliers_inner_loop(fit, cval, result)
        result['ind'] = result.index
        effect = combine_effects(result, n, fit)
        logging.debug(f'calculated effect: {effect}')
        logging.debug(f'calculated result: {result}')

        model = tsa.ARIMA(values_copy - effect, order=arima_order)
        fit = model.fit()

    return (result, stats)


def stage23(
    result: DataFrame,
    fit: tsa.ARIMAResults,
    y: Series,
    cval=0.0,
    arima_order: tuple = (1, 0, 1),
):
    """
    using en-masse method to check effect on model
    """
    if cval == 0:
        n = len(y)
        cval = calc_cval(n)

    result_copy = result.copy()
    for _ in range(1):
        if len(result_copy) == 0:
            logging.info('No potential outliers quiting stage23')
            return
        regressors = get_dataframe_effects(result_copy, len(y), fit)
        logging.debug(result_copy)
        logging.error(regressors)

        model = tsa.ARIMA(y, order=arima_order, exog=regressors)
        fit = model.fit()
        cov = fit.cov_params()

        da = {}
        for col in regressors.columns:
            da[col] = [fit.params[col] / np.sqrt(cov.loc[col, col])]
        df = DataFrame(da)

        logging.debug(df)

        df = abs(df) > cval
        false_columns = df.columns[
            df.apply(lambda col: col.any() == False, axis=0)
        ].to_numpy()

        row_numbers = [
            int(re.search(r'\d+', col).group()) for col in false_columns
        ]

        logging.debug(f'row_numbers {row_numbers}')
        if len(row_numbers) == 0:
            logging.debug('stage2: break')
            break

        result_copy = result_copy.drop(row_numbers)
        logging.debug(result_copy)

    effect = combine_effects(result_copy, len(y), fit)
    model = tsa.ARIMA(y - effect, order=arima_order)
    fit = model.fit()
    return result_copy, effect


def chen_liu(y: Series, cval: float = 0.0, arima_order: tuple = (1, 0, 1)):
    with pd.option_context(
        'display.max_rows', None, 'display.max_columns', None
    ):
        model = tsa.ARIMA(y, order=arima_order)
        fit = model.fit()
        effect = np.zeros(len(y))
        logging.debug(fit.summary())
        (result, stage1stats) = stage1(fit, y, cval)
        if not result.empty:
            (result, effect) = stage23(result, fit, y, cval, arima_order)
            logging.debug(result)
            logging.debug(effect)
        newfit = tsa.ARIMA(y - effect, order=arima_order).fit()
        return result, effect, newfit, stage1stats
