import numpy as np
import chen_liu as cl
from logger import logging

# Generate a time series with outliers.
y = np.random.normal(10, 1, 100)
y[10] = 10
y[40] = -20
y[80] = 10

# Estimate the model parameters and outlier effects using the Chen-Liu algorithm without using the sklearn or outlier_detection libraries.
cl.chen_liu(y)
