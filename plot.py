import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load and parse the results.txt file
with open("results.txt", "r") as file:
    lines = file.readlines()[3:]  # Skip header and separator lines

# Extract data
data = []
for line in lines:
    if line.strip():
        values = line.split()
        m_plus_n = int(values[0])
        time_basic = float(values[1])
        time_efficient = float(values[2])
        memory_basic = int(values[3])
        memory_efficient = int(values[4])
        data.append([m_plus_n, time_basic, time_efficient, memory_basic, memory_efficient])

# Create DataFrame
df = pd.DataFrame(data, columns=["m+n", "Time (Basic)", "Time (Efficient)", "Memory (Basic)", "Memory (Efficient)"])

# Common x-axis for fitted curves
x = np.linspace(df["m+n"].min(), df["m+n"].max(), 200)

# ------------------ Plot 1: Memory Usage ------------------
plt.figure(figsize=(10, 6))
# Linear fit for Efficient algorithm
z1 = np.polyfit(df["m+n"], df["Memory (Efficient)"], 1)
p1 = np.poly1d(z1)
# Quadratic fit for Basic algorithm
z2 = np.polyfit(df["m+n"], df["Memory (Basic)"], 2)
p2 = np.poly1d(z2)

plt.plot(x, p1(x), 'b-', label="Efficient", linewidth=2)
plt.plot(x, p2(x), 'r-', label="Basic", linewidth=2)
plt.scatter(df["m+n"], df["Memory (Efficient)"], color='blue')
plt.scatter(df["m+n"], df["Memory (Basic)"], color='red')
plt.title("m+n vs Memory Usage")
plt.xlabel("m+n")
plt.ylabel("Memory Usage (kB)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("memory_plot.png")  # Save Memory plot as PNG
plt.close()

# ------------------ Plot 2: Execution Time ------------------
plt.figure(figsize=(10, 6))
# Quadratic fits for both algorithms
z3 = np.polyfit(df["m+n"], df["Time (Efficient)"], 2)
p3 = np.poly1d(z3)
z4 = np.polyfit(df["m+n"], df["Time (Basic)"], 2)
p4 = np.poly1d(z4)

plt.plot(x, p3(x), 'b-', label="Efficient", linewidth=2)
plt.plot(x, p4(x), 'r-', label="Basic", linewidth=2)
plt.scatter(df["m+n"], df["Time (Efficient)"], color='blue')
plt.scatter(df["m+n"], df["Time (Basic)"], color='red')
plt.title("m+n vs Execution Time")
plt.xlabel("m+n")
plt.ylabel("Execution Time (ms)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("execution_time_plot.png")  # Save Execution Time plot as PNG
plt.close()

print("Plots have been saved as 'memory_plot.png' and 'execution_time_plot.png'.")