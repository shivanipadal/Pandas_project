import pandas as pd
import numpy as np
from glob import glob
import os
import re

df = pd.read_csv('AK.txt', header=None, names=['State','Gender','Year','Name', 'Count'])
print(df.head())

## The glob module

#  From glob import glob.
# __Find__ all filenames with the structure __"A?.txt"__ in your current directory (? is a single charcter wildcard).
# __Find__ all filenames with the following structure in your current directory and save the resulting list in a variable:

# for root, dir, file in os.walk(r'D:\work related\Shivani\Python\Udemy Pandas project\Project_05_Materials\Part2'):
#     for f in file:
#         print(file)
#         if re.match("A(\w).TXT", file):
#             print(file)
all_files = glob("*.TXT")


A_files = glob('A*.TXT')

print(A_files)

# Importing & merging many Files (complex case)
# __Load__ all files (*.txt) and __merge/concatenate__ all files into one Pandas DataFrame.
# Create a __RangeIndex__ and __save__ the DataFrame (with columns "State", "Gender", "Year", "Name", "Count") in a new csv-file.

dataframes = []
for file in all_files:
    df1 = pd.read_csv(file, header=None, names=['State','Gender','Year','Name', 'Count'])
    dataframes.append(df1)

df = pd.concat(dataframes, ignore_index = True)
print(df)
