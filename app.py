from flask import Flask, render_template, request, redirect, url_for
from data_manager import DataManager
import os
from models import db, Movie

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

data_manager = DataManager()

with app.app_context(): db.create_all()

@app.route('/')
def home():
    all_users = data_manager.get_users()
    return render_template('index.html', user_list=all_users)

@app.route('/users', methods=['POST'])
def add_user():
    usr_name = request.form['usr_name']
    data_manager.create_user(usr_name)
    return redirect(url_for('home'))

@app.route('/users/<int:user_id>/movies', methods=['GET'])
def user_movies(user_id):
    found_movies = data_manager.get_movies(user_id)
    return render_template('movies.html', movie_list=found_movies)



if __name__ == '__main__':
    app.run(port=5002)