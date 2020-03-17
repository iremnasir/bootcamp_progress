import pandas as pd
import numpy as np
import spacy
import re

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from imblearn.under_sampling import RandomUnderSampler, NearMiss
from imblearn.over_sampling import RandomOverSampler, SMOTE
from imblearn.over_sampling import SMOTE
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
from sys import argv
import warnings
warnings.filterwarnings('ignore')


def artist_lyric_dataframe(namelist):
    df = pd.DataFrame() # this is a dictionary of dataframes with name
    for name in namelist:
        df_1 = pd.read_csv(f'{name}.csv', index_col = 0)
        df_1['Artist'] = f'{name}'
        df_1.rename(columns={f'{name}':'Lyrics'}, inplace=True)
        df = pd.concat([df, df_1], axis = 0, ignore_index = True)
    df_lyrics = df.dropna(axis = 0)
    #Styling
    df_lyrics = df_lyrics[~df_lyrics.Lyrics.str.contains("Unfortunately, we are not authorized to show these lyrics")]
    df_lyrics = df_lyrics[~df_lyrics.Lyrics.str.contains("(instrumental)")]
    df_lyrics = df_lyrics[~df_lyrics.Lyrics.str.contains("Instrumental")]
    df_lyrics['Lyrics'] = df_lyrics['Lyrics'].replace(r'\W+|LYRICS|lyrics',' ', regex=True)
    return df_lyrics

def create_a_map(df_lyrics, namelist):
    key = list(range(0,len(namelist)))
    map_dict = dict(zip(namelist, key))
    df_lyrics['ydata'] = df_lyrics['Artist'].map(map_dict)
    return df_lyrics

#
# def train_test(df_lyrics):
#     X_train, X_test, y_train, y_test = train_test_split(df_lyrics[['Song_name','Lyrics', 'Artist']], df_lyrics['ydata'],test_size=0.20, random_state=42)
#     test = pd.concat([X_test, y_test], axis = 1)
#     test.to_csv('Song_Test.csv')
#     return X_train, X_test, y_train, y_test
#
# def lemm(x):
#     model = spacy.load('en_core_web_md')
#     clean = []
#     tokens = model(x)
#     for token in tokens:
#         if not token.is_stop:
#             clean.append(token.lemma_)
#     return " ".join(clean)
#
# def tokenize(X):
#     X['Token'] = X['Lyrics'].apply(lemm)
#     return X
#
#
#
# df_lyrics =artist_lyric_dict(artist_name_re)
# a = organize_df(df_lyrics)
# b = create_a_map(a)
# X_train, X_test, y_train, y_test = train_test(b)
# c = tokenize(X_train)
# print(c)
