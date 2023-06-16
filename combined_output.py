import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df1 = pd.read_csv("Output-8-24.csv")
df2 = pd.read_csv("output-9-4.csv")
df3 = pd.read_csv("output.csv")

combined_df = pd.concat([df1,df2,df3], ignore_index=True)



# combined_df.to_csv("combined_output.csv", index = False)
