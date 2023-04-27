"""
This code takes in monitor data and converts it to a CSV file compatible for Braille_Finger_tracter.py.
"""


import pandas as pd
import numpy as np

# Read in the tab-separated text file
df = pd.read_csv('/Users/by12/Braille/FingerTracker/output_logs/monitor_data/output10_norm.txt', sep='\t')
df = df.rename(columns={'   0.0': 'time', '{}': 'coordinate'})
df = df[df['coordinate'] != '{}']

# Evaluate the coordinate strings
df['coordinate'] = df['coordinate'].apply(lambda x: eval(x))

# Define a function to split the coordinate values in the 'coordinate' column
def split_coordinate_value(coord_dict):
    coord_cols = {}
    for key, value in coord_dict.items():
        coord_cols[f'{key}_X'] = value[0]
        coord_cols[f'{key}_Y'] = value[1]
    return pd.Series(coord_cols)

# Apply the function to the 'coordinate' column to create new columns for each key
df = df.join(df['coordinate'].apply(split_coordinate_value))
df.drop(columns=['coordinate'], inplace=True)
df.head()

# Write the DataFrame to a comma-separated CSV file
df.to_csv('/Users/by12/Braille/FingerTracker/output_logs/monitor_data/test_acc.csv', index=False)
