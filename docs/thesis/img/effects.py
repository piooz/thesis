import matplotlib.pyplot as plt
import numpy as np


def arma2ma(ar, ma, lag_max):
    ar = ar.tolist() if isinstance(ar, np.ndarray) else ar
    ma = ma.tolist() if isinstance(ma, np.ndarray) else ma

    if not isinstance(ar, list):
        ar = [ar]
    if not isinstance(ma, list):
        ma = [ma]

    if len(ar) == 0:
        ar = [1]
    if len(ma) == 0:
        ma = [1]

    p = len(ar)
    q = len(ma)
    m = int(lag_max)

    if m <= 0:
        raise ValueError('Invalid value of lag_max')

    psi = np.zeros(m)
    for i in range(m):
        tmp = ma[i] if i < q else 0.0
        for j in range(min(i + 1, p)):
            tmp += ar[j] * (psi[i - j - 1] if i - j - 1 >= 0 else 1.0)
        psi[i] = tmp

    return psi


def tc_effect(n, ind, w=1, delta=0.7):
    result = np.zeros(n)
    for i in range(0, n - ind):
        result[i + ind] = (delta**i) * w
    return result


def io_effect(n, ind, ar, ma, w=1):
    arr = arma2ma(ar, ma, n - ind - 1)
    arr = np.concatenate([np.zeros(ind), [1], arr])
    return arr * w


# Sample data
x = np.linspace(0, 30)
value_pick = np.zeros(30)
value_pick[10] = 1
level_shift = np.concatenate([np.zeros(10), np.ones(20)])

temporal_changes = tc_effect(30, 10)
innovational = io_effect(30, 10, [1, 0, 0, 1, -1], [-0.6, 0, -0.6, 0.36])

# Create a plot with four line charts
plt.figure(figsize=(10, 10))

# Chart 1: Value Pick
plt.subplot(2, 2, 1)
plt.plot(value_pick, label='Value Pick', color='blue')
plt.title('a', fontsize=20)

# Chart 2: Level Shift
plt.subplot(2, 2, 2)
plt.plot(level_shift, label='Level Shift', color='green')
plt.title('b', fontsize=20)

# Chart 3: Temporal Changes
plt.subplot(2, 2, 3)
plt.plot(temporal_changes, label='Temporal Changes', color='red')
plt.title('c', fontsize=20)

# Chart 4: Straight Value
plt.subplot(2, 2, 4)
plt.plot(innovational, label='Straight Value', color='purple')
# plt.title('IO ARIMA(0,1,1)(0,1,1)')
plt.title('d', fontsize=20)

# Adjust layout for better visualization
plt.tight_layout()

plt.savefig('effects.svg')
# Show the plot
plt.show()
