"""Python class that recommends movies"""
from joblib import load
from model import create_dense, movie_id_dict, mean_rating
import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz
from scipy.spatial import distance



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
    #Find which movies had been rated
    user_mov_index = convert_user_input(user_input_movies, user_input_ratings)
    #Impute the user input ratings.
    #Make a dataframe of user (unchanged) and movie ids
    user_df = pd.DataFrame([user, df_Q.columns], index = ['real', 'movie_ID'])
    user_df = user_df.T
    for mov_id in user_mov_index:
        user_df['real'].loc[user_df['movie_ID'] == mov_id[0]] = mov_id[1]
    #Get user blueprint on movies
    user_blueprint = np.dot(user_df['real'], Q.T)
    prediction = model.inverse_transform(user_blueprint)
    #Concat the dataframes
    user_df['predicted'] = prediction
    user_df['predicted'] = user_df['predicted'].astype(int)
    #Round the values
    user_df['real'] = user_df['real'].round(3)
    mean_rating_round = round(mean_rating_1, ndigits = 3)
    #Filter unwatched movies based on high-precision digit (non)matching
    user_df = user_df[user_df['real']==mean_rating_round]
    #Sort for recommendation
    recomm_for_user = user_df.sort_values(by = 'predicted', ascending = False)
    #Map the movie ids
    movies_ = recomm_for_user['movie_ID'].map(movie_id_dict)
    #Restrict the number
    movies_ = movies_.head(number_of_recomm)
    movies_list = list(movies_)
    return movies_list

def cosine_similarity(number_of_recomm, user_input_movies, user_input_ratings):
    #Create the mean-filled dense_matrix
    dense_matrix = create_dense()
    #Create the user array
    mean_rating_1 = mean_rating()
    user = np.repeat(mean_rating_1, dense_matrix.shape[1])
    user_df = pd.DataFrame([user], columns = dense_matrix.columns)
    #Collect user input
    user_mov_index = convert_user_input(user_input_movies, user_input_ratings)
    #Impute user ratings
    for mov_id in user_mov_index:
        user_df[mov_id[0]] = mov_id[1]
    #Append it to the original user_movie_matrix
    dense_matrix_user = pd.concat([dense_matrix, user_df], ignore_index=False)
    #Create user-user sparse matrix
    UU = np.zeros((len(dense_matrix_user), len(dense_matrix_user)))
    UU = pd.DataFrame(UU, index=dense_matrix_user.index, columns=dense_matrix_user.index)
    # calculate pairwise similarities
    for u in UU.index:
        for v in UU.columns:
        # 2. step: calculate similarities
            UU.loc[u, v] = 1-distance.correlation(dense_matrix_user.loc[u],
                                                    dense_matrix_user.loc[v])
    active_user = 0
    # find similarities for active_user and sort it, take 1 to 5 entries
    # entry at 0 contains the similrity with itself
    neighbors = UU.loc[active_user].sort_values(ascending=False)[1:6]
    #Final matrix
    neighbors_m = dense_matrix_user.loc[neighbors.index]
    #Take the first user and suggest movies that person liked
    movies_list = list(neighbors_m.iloc[0].sort_values(ascending = False)
                        .head(number_of_recomm).index.map(movie_id_dict))
    return movies_list
