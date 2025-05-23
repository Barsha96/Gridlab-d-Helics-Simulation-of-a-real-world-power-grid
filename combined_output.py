import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df1 = pd.read_csv("output1.csv")
df2 = pd.read_csv("output2.csv")
df3 = pd.read_csv("output3.csv")
df4 = pd.read_csv("output4.csv")
df5 = pd.read_csv("output.csv")

combined_df = pd.concat([df1,df2,df3,df4,df5], ignore_index=True)

combined_df.to_csv("combined_output5.csv", index = False)
