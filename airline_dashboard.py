import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Simulated turnaround time (in minutes)
data = pd.Series(np.random.normal(35, 5, size=100))

# Calculate control limits
mean = data.mean()
std = data.std()
ucl = mean + 3 * std
lcl = mean - 3 * std

# Plot control chart
plt.figure(figsize=(12, 5))
plt.plot(data, marker='o', label='Turnaround Time')
plt.axhline(mean, color='green', linestyle='--', label='Mean')
plt.axhline(ucl, color='red', linestyle='--', label='UCL')
plt.axhline(lcl, color='red', linestyle='--', label='LCL')
plt.title('Flight Turnaround Time – Control Chart')
plt.xlabel('Flight Event')
plt.ylabel('Minutes')
plt.legend()
plt.grid(True)
plt.show()
