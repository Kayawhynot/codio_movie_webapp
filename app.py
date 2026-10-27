import requests
from flask import Flask, render_template, request, redirect, url_for
from data_manager import DataManager
import os
from dotenv import load_dotenv
from models import db, Movie
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()
OMDB_API_KEY = os.getenv('OMDB_API_KEY')

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

data_manager = DataManager()

os.makedirs(os.path.join(basedir, 'data'), exist_ok=True)

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    """Show the start page with all users."""
    all_users = data_manager.get_users()
    return render_template('index.html', user_list=all_users)


@app.route('/users', methods=['POST'])
def add_user():
    """Create a new user from the form and go back to the start page."""
    usr_name = request.form['usr_name']
    data_manager.create_user(usr_name)
    return redirect(url_for('home'))


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def user_movies(user_id):
    """Show all movies of one user."""
    found_movies = data_manager.get_movies(user_id)
    return render_template('movies.html', movie_list=found_movies, page_user_id=user_id)


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def save_movie(user_id):
    """Look up a title on OMDb and save the movie for the user.

    Shows a hint instead if OMDb has no match, cannot be reached or the
    database fails.
    """
    title = request.form['title']
    try:
        response = requests.get(
            'https://www.omdbapi.com/',
            params={'apikey': OMDB_API_KEY, 't': title, 'type': 'movie'},
            timeout=5
        )

        movie_data = response.json()
    except requests.exceptions.RequestException:
        found_movies = data_manager.get_movies(user_id)
        return render_template('movies.html', movie_list=found_movies, page_user_id=user_id,
                               error_message='Movie DB is temporarily not available')
    if 'Error' in movie_data:
        found_movies = data_manager.get_movies(user_id)
        return render_template('movies.html', movie_list=found_movies, page_user_id=user_id,
                               error_message=movie_data['Error'])
    new_movie = Movie(
        mv_title=movie_data['Title'],
        mv_release_yr=movie_data['Year'],
        mv_director=movie_data['Director'],
        mv_poster=movie_data['Poster'],
        user_id=user_id
    )
    try:
        data_manager.add_movie(new_movie)
        return redirect(url_for('user_movies', user_id=user_id))
    except SQLAlchemyError:
        db.session.rollback()
        found_movies = data_manager.get_movies(user_id)
        return render_template('movies.html', movie_list=found_movies, page_user_id=user_id,
                               error_message='New Movie could not be added please try again')


@app.route('/users/<int:user_id>/movies/<int:mv_id>/delete', methods=['POST'])
def remove_movie(user_id, mv_id):
    """Delete one movie and return to the movie list."""
    data_manager.delete_movie(mv_id)
    return redirect(url_for('user_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:mv_id>/update', methods=['POST'])
def rename_movie(user_id, mv_id):
    """Change the title of one movie and return to the movie list."""
    new_title = request.form['upd_mv_name']
    data_manager.update_movie(mv_id, new_title)
    return redirect(url_for('user_movies', user_id=user_id))


@app.errorhandler(404)
def page_not_found(e):
    """Show the custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(port=5002)
