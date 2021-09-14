import os
import numpy as np
import pandas as pd

ser_files = [f for f in os.listdir('.') if f.endswith('.ser')]
if len(ser_files) != 1:
    raise ValueError('There should be a single .ser file in the current directory')

filename = ser_files[0]

with open(filename, 'r') as f:
    ser = f.read()
zcont = input("Enter name of z-trace that you want to output ")
# find index range for searched z-trace and save only zpoints to a new string
if zcont in ser:
    a = ser.find(zcont)
    temp_str = ser[a:]
    b = temp_str.find('"/>')
    temp_str = temp_str[:b]
    c = temp_str.find('points="')
    temp_str = temp_str[c:]
    zpoints_raw = temp_str[8:]
else:
    print("Z-trace not found")

# remove tabs, commas, and new lines from string
zpoints_clean = zpoints_raw.replace('\t', '').replace(',', ' ').replace('\n', ' ')
# split string into list of strings using space delimiter
zpoints_split = zpoints_clean.split()
# convert list of strings into a list containing floats for x,y points and ints for sec number
zpoints = [int(i) if i.isdigit() else float(i) for i in zpoints_split]

# convert list into an array and store in 'num' variable
num = np.array(zpoints)
# convert this 1-D array to 2-D array with 3 columns and an undefined (-1) number of rows
reshaped = num.reshape(-1,3)
# construct a table with 3 named columns for our data
output = pd.DataFrame(reshaped, columns=['x','y','sec'])

# list columns we want to rearrange in our dataframe
cols = output.columns.tolist()
# rearrange columns, this moves the last element to the first position, now ['sec','x','y']
cols = cols[-1:] + cols[:-1 ]
# this now reorders the entire dataframe
output = output[cols]

# export to csv
output.to_csv(zcont+'_output.csv', index = None)