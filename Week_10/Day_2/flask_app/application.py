from flask import Flask, render_template, request
from recommender import user_recommendation, user
import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)
# make this file the center of the app
# We launch this file from the terminal to start the app


@app.route('/index')  # whatever the function below this, route it to the path
def hello_world():
    return render_template('index.html')  # it automatically looks at templates


@app.route('/recommender')
def recommender():
    user_input = dict(request.args)
    user_input_movies = list(user_input.values())[::2]
    user_input_ratings = list(user_input.values())[1::2]
    user_input = zip(user_input_movies, user_input_ratings)




    result = user_recommendation(user_input_movies, 10)
    return render_template('recommender.html', result=result, user_input=user_input)
