import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    'loadtest.csv',
    header=None,
    names=[
        'timestamp',
        'code',
        'latency',
        'bytesout',
        'bytesin',
        'error',
        'rate',
    ],
    index_col=[0],
)

lat = df['latency']

plt.plot(lat)
plt.show()
