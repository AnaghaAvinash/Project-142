#importing numpy and pandas
import pandas as pd
import numpy as np

#Reading the articles.csv file into a DataFrame
df = pd.read_csv('articles.csv')

#Sorting the rows based on total_events column in ascending order
df = df.sort_values(['total_events'], ascending=[False])

#Creating an output with top 20 rows.
output = df[["url", "title", "text", "lang", "total_events"]].head(20).values.tolist()