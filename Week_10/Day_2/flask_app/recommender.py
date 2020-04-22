"""Python class that recommends movies"""
from joblib import load
from model import create_dense, movie_id_dict, mean_rating
import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz



#Load the pretrained model
def get_model():
    trained_NMF = load('NMF.joblib')
    return trained_NMF

def convert_user_input(user_input_movies, user_input_ratings):
    #Get the indexes of movies entered by user
    user_movie_index = []
    user_dict = dict(zip(user_input_movies, user_input_ratings))
    for movie in user_dict:
        movie_low = str(movie).lower()
        # go through the dictionary and find fuzzy matches of user input
        for ind, m in movie_id_dict.items():
            if fuzz.token_sort_ratio(movie_low, m) > 90:
                user_movie_index.append([ind, float(user_dict[movie])])
                break
    if len(user_movie_index) != len(user_input_movies):
        unknown = len(user_input_movies) - len(user_movie_index)
        print(f'I could not find {unknown} movie(s) from your list')
    return user_movie_index


def user_recommendation(number_of_recomm, user_input_movies, user_input_ratings):
    model = get_model()
    dense_matrix = create_dense()
    #Convert component-movie matrix to df
    Q = model.components_
    df_Q = pd.DataFrame(data = Q, columns = dense_matrix.columns)
    #Convert user input to an array
    mean_rating_1 = mean_rating()
    user = np.repeat(mean_rating_1, Q.shape[1])
    user_mov_index = convert_user_input(user_input_movies, user_input_ratings)
    #Impute the user input ratings.
    for mov_index in user_mov_index:
    #i.e Toy Story is movie nr 1 but at index 0 hence -1 below
        user[mov_index[0]-1] = mov_index[1]
    #Get user blueprint on movies
    user_blueprint = np.dot(user, Q.T)
    prediction = model.inverse_transform(user_blueprint)
    print(prediction.shape)
    #Create a dataframe of user array and movieID
    user_df = pd.DataFrame([user, df_Q.columns, prediction], index = ['real', 'movie_ID', 'predicted'])
    user_df = user_df.T
    user_df['movie_ID'] = user_df['movie_ID'].astype(int)
    print(user_df)
    #Round the values
    user_df['real'] = user_df['real'].round(3)
    #print(user_df.loc[user_df['real'] == 2.0])
    #print(user_df.loc[user_df['real'] == 3.0])
    #print(user_df.loc[user_df['real'] == 1.0])
    #print(user_df.index)


    mean_rating_round = round(mean_rating_1, ndigits = 3)
    #Filter unwatched movies
    user_df = user_df[user_df['real']==mean_rating_round]
    #Sort for recommendation
    recomm_for_user = user_df.sort_values(by = 'predicted', ascending = False)
    print(recomm_for_user)
    #Map the movie ids
    movies_ = recomm_for_user['movie_ID'].map(movie_id_dict)
    #Restrict the number
    movies_ = movies_.head(number_of_recomm)
    movies_list = list(movies_)
    return movies_list

movies = ['Matrix, The', 'Toy Story','Shawshank Redemption', ]
ratings = ['3', '2', '1']
print(user_recommendation(10, movies, ratings))
