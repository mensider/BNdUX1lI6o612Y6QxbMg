#!/usr/bin/env python
# coding: utf-8

# In[12]:


# The function returns a pandas dataframe
import pandas as pd

def parseCsv(fileloc):
    # Reading the csv file
    df =pd.read_excel(fileloc)
    # Extracting out only the required columns
    df = df[['Shipment', 'Induct Station', 'Destination']].copy()
    return df

# Fill in the absolute path within quotes here
myVal =parseCsv('./data/sampleData.csv')
print(myVal)
