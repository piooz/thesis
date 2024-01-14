import numpy as np
import chen_liu as cl
from logger import logging

if __name__ == '__main__':
    # Generate a time series with outliers.
    # y = np.random.normal(10, 1, 100)
    y = np.repeat(10, 100)
    y[40] = -200
    logging.debug(y)

    # Estimate the model parameters and outlier effects using the Chen-Liu algorithm without using the sklearn or outlier_detection libraries.
    cl.chen_liu(y)
