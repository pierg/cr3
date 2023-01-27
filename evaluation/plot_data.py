import matplotlib.pyplot as plt
import numpy as np

from scipy.interpolate import interp1d

# Define the x, ya, and yb lists
x = [1, 2, 3, 4, 5]
ya = [2, 3, 4, 5, 6]
yb = [1, 4, 5, 8, 11]

# Interpolate the data using a linear interpolation method
f_ya = interp1d(x, ya, kind='linear')
f_yb = interp1d(x, yb, kind='linear')

# Create a new set of x values for the interpolated data
xnew = np.linspace(min(x), max(x), num=100, endpoint=True)

# Use the interpolated functions to get the y values for the new x values
ynew_ya = f_ya(xnew)
ynew_yb = f_yb(xnew)

# Plot the interpolated data
plt.plot(xnew, ynew_ya, '-', label='ya')
plt.plot(xnew, ynew_yb, '-', label='yb')

# Add labels and a legend to the plot
plt.xlabel('x')
plt.ylabel('y')
plt.legend()

# Show the plot
plt.show()
