import numpy as np
import matplotlib.pyplot as plt

# Generate data
np.random.seed(42)
num_points = 50
x_bottom_left = np.random.rand(num_points) * 0.3
y_bottom_left = np.random.rand(num_points) * 0.3

x_center_outlier = [0.5]  # Center outlier
y_center_outlier = [0.5]

x_top_right_outlier = [0.8]  # Top-right outlier
y_top_right_outlier = [0.8]

# Create scatter plot
plt.scatter(
    x_bottom_left, y_bottom_left, color='blue', label='Bottom-Left Points'
)
plt.scatter(x_center_outlier, y_center_outlier, color='red', label='x1')
plt.scatter(
    x_top_right_outlier, y_top_right_outlier, color='green', label='x2'
)

# Customize the plot
# plt.title('Scatter Plot with Outliers')
# Disable numeric labels on scales
plt.tick_params(
    axis='both',
    which='both',
    bottom=False,
    top=False,
    left=False,
    right=False,
    labelbottom=False,
    labelleft=False,
)

# Annotate the outliers
plt.annotate(
    'x1',
    (x_center_outlier[0], y_center_outlier[0]),
    textcoords='offset points',
    xytext=(-10, 5),
    ha='center',
    fontsize=14,
    color='red',
)
plt.annotate(
    'x2',
    (x_top_right_outlier[0], y_top_right_outlier[0]),
    textcoords='offset points',
    xytext=(-10, -25),
    ha='center',
    fontsize=14,
    color='green',
)

# Show the plot
plt.savefig('masking.svg')
