import pandas as pd
import numpy as np

### Importing one File & Understanding the Data Structure

# 1. __Load__ the file __"yob1880.txt"__ into Pandas and __inspect__.

df=pd.read_csv('yob1880.txt', header=None, names = ["Name", "Gender", "Count"])

# print(df.head(10))

# 3. __Load__ all files (yob????.txt) and __merge/concatenate__ all files into one Pandas DataFrame. 
# Make sure you add the __column "Year"__.

df_1880 = pd.read_csv("yob1880.txt", header = None, names = ["Name", "Gender", "Count"])
df_1881 = pd.read_csv("yob1881.txt", header = None, names = ["Name", "Gender", "Count"])

# print(df_1880, df_1881)

# print(pd.concat(objs = [df_1880, df_1881], axis = 0, keys = [1880, 1881], names = ["Year"]))

# print(pd.concat(objs = [df_1880, df_1881], axis = 0, keys = [1880, 1881],
        #   names = ["Year"]).droplevel(-1).reset_index())

years=list(range(1880, 2019))

dataframe = []
for year in years:
    df1=pd.read_csv(f'yob{year}.txt', header=None, names=['Name', 'Gender', 'Count'])
    dataframe.append(df1)

# df2 = pd.concat(dataframe, keys=years, axis=0, names=['Year'])
df = pd.concat(dataframe, keys=years, axis=0, names=['Year']).droplevel(-1).reset_index()

# print(df2)
print(df)