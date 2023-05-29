import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df = pd.read_csv("out11.csv")
print(df)

property_name = "measured_power_A"  # Replace "voltage_A" with the desired property name
property_data = df[df["property"] == property_name]

print(property_data)

property_data["time"] = pd.to_datetime(property_data["time"])

plt.plot(property_data["time"], property_data["complex_value"].apply(lambda x: complex(x).real))
plt.xlabel("Time")
plt.ylabel(property_name)
plt.title("Time Sequence of {}".format(property_name))
plt.show()