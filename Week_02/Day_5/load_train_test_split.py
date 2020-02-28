#Import necessary modules

from sys import argv
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

#Name of .csv files
namelist = argv[1:]

#Read two data sets and put them into two different DFs
df_p = pd.read_csv(namelist[0], index_col = 0)
df_py = pd.read_csv(namelist[1], index_col = 0)

#Check shapes

if len(df_p) != len(df_py):
    print("DataFrames aren't of equal length")

#Merging pumps_y as a new column on pumps
df_p['status_group'] = df_py['status_group']

#Do train/test split
Xtrain, Xtest, ytrain, ytest = train_test_split(df_p.loc[:,'amount_tsh':'waterpoint_type_group'], df_p.loc[:,'status_group'], test_size = 0.2, random_state = 42)
Xtrain.to_csv('Xtrain.csv', index_label = 'id')
Xtest.to_csv('Xtest.csv', index_label = 'id')
ytrain.to_csv('ytrain.csv', header = False, index_label =  'id')
ytest.to_csv('ytest.csv',header = False, index_label =  'id')

print('Train and test split is done!. Move on to feature eng. and fitting...')
