import numpy as np
import pandas as pd
from pandas import DataFrame
import statsmodels.tsa.arima.model as tsa
import statsmodels.api as sm
import matplotlib.pyplot as plt
from effects import combine_effects, get_dataframe_effects
import xii
import re
from logger import logging


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
        result_df = result_df._append(
            {
                'ind': ind,
                'type': max_col,
                'tstat': max_value,
                'coefhat': coefhat,
            },
            ignore_index=True,
        )
    return DataFrame(result_df[result_df['tstat'].abs() >= cval])


def extract_values(row, cval=3):
    types = ['IO', 'AO', 'LS', 'TC']
    t_values = [row[f'{type}tstat'] for type in types]

    # Find types where absolute value of t is greater than 3
    valid_types = [
        types[i] for i in range(len(types)) if abs(t_values[i]) > cval
    ]

    if not valid_types:
        return pd.Series({'type': None, 'coefhat': None, 'tstat': None})

    # Find the type with the maximum absolute value of t
    max_type = max(valid_types, key=lambda t: abs(row[f'{t}tstat']))

    return pd.Series(
        {
            'type': max_type,
            'coefhat': row[f'{max_type}coef'],
            'tstat': row[f'{max_type}tstat'],
        }
    )


def locate_outliers_inner_loop(fit, cval):
    stats = xii.tstat(fit)
    outliers = stats.apply(extract_values, cval=cval, axis=1)
    outliers = outliers.dropna()
    logging.debug(stats)
    return outliers


def stage1(fit, values, cval=0):
    n = len(values)
    if cval == 0:
        if n < 50:
            cval = 3
        elif n > 450:
            cval = 4
        else:
            cval = 3 + 0.0025 * (n - 50)

    plt.plot(values)

    result = None
    effect = None
    for _ in range(1):
        result = locate_outliers_inner_loop(fit, cval)
        result['ind'] = result.index
        effect = combine_effects(result, n, fit)
        logging.debug(effect)
        # plt.plot(effect)
        plt.plot(values - effect)

    return result, effect


def stage2(result: DataFrame, fit, y, cval=3.0):
    """
    using en-masse method, whatever it is.
    """
    result_copy = result.copy()
    for _ in range(1):
        if len(result_copy) == 0:
            return
        regressors = get_dataframe_effects(result_copy, len(y), fit)
        logging.debug(result_copy)

        model = tsa.ARIMA(y, order=(1, 0, 1), exog=regressors)
        fit = model.fit()
        cov = fit.cov_params()

        df = DataFrame()
        for col in regressors.columns:
            df[col] = [fit.params[col] / np.sqrt(cov.loc[col, col])]

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
    return result_copy


def chen_liu(y):
    with pd.option_context(
        'display.max_rows', None, 'display.max_columns', None
    ):
        y = sm.datasets.nile.data.load_pandas().data['volume']
        model = tsa.ARIMA(y, order=(1, 0, 1))
        fit = model.fit()
        result, effect1 = stage1(fit, y, 2.2)
        logging.debug(result)
        stage2(result, fit, y, 2.2)
