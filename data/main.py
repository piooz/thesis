from datetime import datetime
import pandas as pd
from chenLiu import *
import os
import matplotlib.pyplot as plt
from tsf2df import convert_tsf_to_dataframe
import statsmodels.tsa.arima.model as tsa
import psutil
import time
import numpy as np


MODULE_DIR = os.path.dirname(__file__)


def measure_function_performance(func, *args, **kwargs):
    start_time = time.time()
    process = psutil.Process()
    start_memory = process.memory_info().rss / 1024  # in KB

    result = func(*args, **kwargs)

    end_time = time.time()
    end_memory = process.memory_info().rss / 1024  # in KB

    execution_time = end_time - start_time
    memory_usage = end_memory - start_memory

    print(
        f"Execution time for '{func.__name__}': {execution_time:.4f} seconds"
    )
    print(f"Memory usage for '{func.__name__}': {memory_usage:.2f} KB")

    return result


def plot_time_series_with_points(
    origin, fixed, df, fit: tsa.ARIMAResults, dataset_name: str
):
    plt.figure(figsize=(10, 6))

    # Plot the first time series in gray
    plt.plot(origin, color='gray', label='Origin')

    # Plot the second time series
    plt.plot(fixed, color='blue', label='Correct')

    origin_series = pd.Series([origin[i] for i in df.index], index=df.index)
    plt.scatter(df.index , origin_series, color='red', label='Outliers')
    # Add points to the second time series
    # plt.scatter(points.index, points.values, color='red', label='Points')

    # Set labels and title
    plt.xlabel('Czas', fontsize=13)
    plt.ylabel('Wartość', fontsize=13)

    # print(f"{fit.model_orders['ar']}")
    title = f"{dataset_name}: ARIMA({fit.model_orders['ar']}, {fit.model_orders['trend']}, {fit.model_orders['ma']})"
    plt.title(title)

    # Add legend
    plt.legend()

    date = datetime.now().strftime('%d-%m-%Y-%H-%M-%S')
    plt.savefig(f'outfigures/{dataset_name}-{date}.svg')

    print(df)
    # Show plot
    plt.show()


def load_module_tsf(file: str, index: int):
    (
        loaded_data,
        frequency,
        forecast_horizon,
        contain_missing_values,
        contain_equal_length,
    ) = convert_tsf_to_dataframe(f'{MODULE_DIR}/{file}')
    return pd.Series(loaded_data['series_value'][index])


def test_covid_poland():
    df = pd.read_csv(f'{MODULE_DIR}/covid-cumulative-deaths.csv')
    # Filter the DataFrame to include only rows where the Country/Region is 'Poland'
    poland_data = df[df['Country/Region'] == 'Poland']
    arr = pd.to_numeric(poland_data.iloc[0][4:400])
    arr = arr.to_list()
    print(arr)

    (raport, series, effect, fit) = measure_function_performance(
        chenLiu.chen_liu, cval=3, arima_order=(3, 0, 2), y=arr
    )
    print(raport)
    plot_time_series_with_points(
        arr, series, raport, fit, 'Cumulative deaths COVID-19 Poland'
    )


def test_cif():
    arr = load_module_tsf('cif_2016_dataset.tsf', 0)
    print(arr)

    (raport, series, effect, fit) = measure_function_performance(
        chenLiu.chen_liu, y=arr, cval=2, arima_order=(2, 0, 2)
    )
    print(series)
    plot_time_series_with_points(arr, series, raport, fit, 'CIF')


def test_iot_sensor_temp():
    df = pd.read_csv(f'{MODULE_DIR}/iot_sensor/Occupancy.csv')
    arr = df['Temperature'][:200]
    # Step 2: Generate spikes
    spike_positions = np.random.choice(200, 1, replace=False)

    # Step 3: Generate random spikes with both positive and negative values
    spikes = np.random.choice([-1, 1,2,-2], 1)

    for pos, spike in zip(spike_positions, spikes):
        arr[pos] += spike

    (raport, series, effect, fit) = measure_function_performance(
        chenLiu.chen_liu, y=arr, cval=0.7, arima_order=(1, 0, 1)
    )

    print(series)
    plot_time_series_with_points(
        arr, series, raport, fit, 'IOT sensor temperature'
    )


def test_iot_sensor_humidity():
    df = pd.read_csv(f'{MODULE_DIR}/iot_sensor/Occupancy.csv')
    arr = df['Humidity'][:200]

    (raport, series, effect, fit) = measure_function_performance(
        chenLiu.chen_liu, y=arr, cval=2, arima_order=(1, 0, 2)
    )

    print(series)
    plot_time_series_with_points(
        arr, series, raport, fit, 'IOT sensor humdity'
    )


def test_netflix():
    df = pd.read_csv(f'{MODULE_DIR}/NFLX.csv')
    print(df['Open'].iloc[100:200])
    arr = df['Open'].iloc[100:200].reset_index(drop=True)

    (raport, series, effect, fit) = measure_function_performance(
        chenLiu.chen_liu, y=arr, cval=2, arima_order=(1, 0, 2)
    )

    print(series)
    plot_time_series_with_points(
        arr,
        series,
        raport,
        fit,
        'Netflix open stock price from 2018-06-27 to 2018-11-16',
    )


def test_ETD_temp():
    df = pd.read_csv(f'{MODULE_DIR}/ETDataset/ETT-small/ETTm1.csv')
    arr = df['OT'].iloc[1470:1770].reset_index(drop=True)
    print(arr)

    (raport, series, effect, fit) = measure_function_performance(
        chenLiu.chen_liu, y=arr, cval=3, arima_order=(1, 0, 2)
    )

    print(series)
    plot_time_series_with_points(
        arr,
        series,
        raport,
        fit,
        'Oil temperature from 2016-07-16 07:00:00 to 2016-07-19 10:00:00 (15 min. step)',
    )


def test_ETD_load():
    df = pd.read_csv(f'{MODULE_DIR}/ETDataset/ETT-small/ETTm1.csv')
    arr = df['MUFL'].iloc[1470:1770].reset_index(drop=True)
    print(arr)

    (raport, series, effect, fit) = measure_function_performance(
        chenLiu.chen_liu, y=arr, cval=3, arima_order=(1, 0, 2)
    )

    print(series)
    plot_time_series_with_points(
        arr,
        series,
        raport,
        fit,
        'Oil Load from 2016-07-16 07:00:00 to 2016-07-19 10:00:00 (15 min. step)',
    )


def test_weather():
    df = pd.read_csv(f'{MODULE_DIR}/rain.csv')
    arr = df['data']
    (raport, series, effect, fit) = measure_function_performance(
        chenLiu.chen_liu, y=arr, cval=5, arima_order=(1, 0, 1)
    )

    plot_time_series_with_points(
        arr,
        series,
        raport,
        fit,
        'rain dataset'
    )


#
#
# def test_covid():
#     arr = load_module_tsf('covid_deaths_dataset.tsf', 0)
#
#     (res, effect, fit, stats) = measure_function_performance(
#         al.chen_liu, arr, cval=2, arima_order=(3, 1, 2)
#     )
#     print(res)
#     plot_time_series_with_points(arr, arr - effect, res, fit, 'covid deaths')
#
#


def test_dominick0():
    arr = load_module_tsf('dominick_dataset.tsf', 0)

    (raport, series, effect, fit) = measure_function_performance(
        chenLiu.chen_liu, y=arr, cval=2, arima_order=(1, 0, 2)
    )
    print(raport)
    plot_time_series_with_points(arr, series, raport, fit, 'Dominick 1')


# def test_dominick10():
#     arr = load_module_tsf('dominick_dataset.tsf', 10)
#
#     (raport, series, effect, fit) = measure_function_performance(
#         chenLiu.chen_liu, y=arr, cval=2, arima_order=(1, 0, 2)
#     )
#     print(raport)
#     plot_time_series_with_points(arr, series, raport, fit, 'dominick 10')


def testNile():
    df = pd.read_csv(f'{MODULE_DIR}/Nile.csv', header=None)
    print(df[0])
    (raport, series, effect, fit) = measure_function_performance(
        chenLiu.chen_liu, cval=2, arima_order=(1, 0, 1), y=df[0]
    )
    plot_time_series_with_points(df[0], df[0] - effect, raport, fit, 'Nile')
    # eff = measure_function_performance(
    #     chenLiu.chen_liu,
    #     y=df[0],
    #     cval=1.9,
    #     arima_order=(1, 0, 1),
    #     chunks=2,
    # )
    # print(eff)


if __name__ == '__main__':

    with pd.option_context(
        'display.max_rows', None, 'display.max_columns', None
    ):
        # testNile()   # passed
        # test_cif()
        # test_iot_sensor_temp()
        # test_iot_sensor_humidity()
        # test_netflix()
        # test_ETD_temp()
        # # test_ETD_load()
        test_weather()
        # test_dominick10()
        # test_dominick0()
        # test_covid_poland()
