import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import pickle
import json
import os
from sys import argv


namelist = argv[1:]
print(namelist)
#Create an Artist name pattern
artist_name_re=[]
for name in namelist:
    artist_name = str(name).lower()
    artist_name_re.append(re.sub('_','-',artist_name))


loc = '/Users/iremn/PythonClass/Spiced/gradient_garlic-code_Work/Week_04/Day_5/'
os.chdir(loc)
def dataframe_artists(namelist, loc):
    for artist_name_re in namelist:
        df_ = []
        sn = []
        data = []
        path = loc+artist_name_re
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f))]
        for f in files:
            with open(os.path.join(path,f),'r') as myfile:
                data.append(myfile.read())
                sn.append(str(f).strip())
                obj = zip(sn, data)
            df_ = pd.DataFrame(obj, columns = ['Song_name', f'{artist_name_re}'])

            df_['Song_name'] = df_['Song_name'].str.replace(r'(\.)(txt)$', '')
            df_['Song_name'] = df_['Song_name'].str.replace(f'{artist_name_re}', '')
            df_['Song_name'] = df_['Song_name'].str.replace('-', ' ')
            df_['Song_name'] = df_['Song_name'].str.replace('lyrics', ' ')
            df_[f'{artist_name_re}'] = df_[f'{artist_name_re}'].str.strip('[')
            df_[f'{artist_name_re}'] = df_[f'{artist_name_re}'].str.strip(']')
            df_ = df_.replace(r'\\n',' ', regex=True)

            df_.to_csv(f'{artist_name_re}.csv')

dataframe_artists(artist_name_re, loc)
