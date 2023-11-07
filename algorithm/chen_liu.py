import numpy as np
from pandas import DataFrame
import statsmodels.tsa.arima.model as tsa
import statsmodels.api as sm

def calc_pi_coeff(fit):
    # Multiply the two polynomials
    result_poly = np.polymul(fit.polynomial_ma, fit.polynomial_ar)
    result_poly = np.append([1],  result_poly)
    # result_poly = np.polydiv(result_poly, fit.polynomial_trend)

    # Print the coefficients of the result polynomial
    print("Resulting Polynomial Coefficients:", result_poly)
    return result_poly

def calc_tstats(model, sigma):
    pi_coeff = calc_pi_coeff(model)

    filtr = (sm.tsa.filters.convolution_filter(model.resid , np.flip(model.polynomial_ma), 1))
    print (filtr)
    print (model.resid)
    print(len(filtr))

    df = DataFrame(columns=['type', 'tstat'])
    return df

def locate_outliers_inner_loop(model):

    sigma = model.mae * 1.483
    df = calc_tstats(model, sigma)

    pass


def stage1(y , model, cval = 3):
    n = len(y)

    if cval == 0:
        if (n < 50):
            cval = 3
        elif (n > 450):
            cval = 4
        else:
            cval = 3 + 0.0025*(n - 50)

    for _ in range(1):
        _ = locate_outliers_inner_loop(model)

        pass



    return 

def chen_liu(y):
    """
    Chen-Liu algorithm for joint estimation of model parameters and outlier effects in time series.

    Args:
        y: Time series data.
        model: A model object that can be fitted to time series data.
        max_iter: Maximum number of iterations.

    Returns:
        model_params: Estimated model parameters.
        outlier_effects: Estimated outlier effects.
    """


    df = DataFrame(y)
    df['time'] = np.arange(len(df.index))

    model = tsa.ARIMA(y, order=(1,1,1))
    fit = model.fit()



    ehe1 = stage1(y, fit)








# def arima2ma(arimafit):
#
#     ma_coefs = arimafit.polynomial_ma
#     ma_model = sm.tsa.arima.ARIMA([], order=(0,0, len(ma_coefs)))
#     ma_model.polynomial_ma = ma_coefs
#
#     return ma_model
#


def t_stat(fit):
    # Calculate the t-statistics for the residuals
    t_stats = fit.resid / np.std(fit.resid)
    return t_stat
