import numpy as np
import statsmodels.api as sm


def arima2poly(arima_model, order, seasonal_order):
    ar_params = arima_model.arparams
    ma_params = arima_model.maparams
    d = order[1]
    seasonal_order = seasonal_order

    if seasonal_order is not None:
        s = seasonal_order[3]
        seasonal_ar_params = arima_model.seasonalarparams
        seasonal_ma_params = arima_model.seasonalmaparams
        ar_params = np.concatenate([ar_params, np.zeros(s - 1)])
        ma_params = np.concatenate([ma_params, np.zeros(s - 1)])
        for i in range(1, s):
            ar_params[i * (d + 1):] += seasonal_ar_params[:len(ar_params) - i * (d + 1)]
            ma_params[i * (d + 1):] += seasonal_ma_params[:len(ma_params) - i * (d + 1)]

    # Stwórz współczynniki wielomianu z AR i MA
    ar_poly = np.poly1d(np.concatenate([[1], -ar_params]))
    ma_poly = np.poly1d(np.concatenate([[1], ma_params]))

    # Zwróć iloczyn AR i MA jako współczynniki wielomianu
    poly_coeffs = np.convolve(ar_poly.coeffs, ma_poly.coeffs)

    return poly_coeffs

if __name__ == "__main__":

    y = (sm.datasets.nile.data.load_pandas().data['volume'])
    # y = sm.datasets.get_rdataset('Nile').raw_data['value']
    # df = pd.DataFrame(y)
    # plt.plot(y)
    # df['time'] = np.arange(len(df.index))
    model = sm.tsa.ARIMA(y, order=(0,1,1))
    fit = model.fit()
    print(arima2poly( fit, (0,1,1), None ))

    pass
