from models import db, User, Movie


class DataManager:
    """Reads and writes users and movies in the database."""

    def create_user(self, usr_name):
        """Save a new user with the given name."""
        new_user = User(name=usr_name)
        db.session.add(new_user)
        db.session.commit()

    def get_users(self):
        """Return all users."""
        return User.query.all()

    def get_movies(self, user_srch_id):
        """Return all movies of the user with the given id."""
        return Movie.query.filter_by(user_id=user_srch_id).all()

    def add_movie(self, movie_data):
        """Save a Movie object in the database."""
        db.session.add(movie_data)
        db.session.commit()

    def update_movie(self, movie_id, new_movie):
        """Set a new title for the movie with the given id."""
        updated_mv = Movie.query.filter_by(mv_id=movie_id).first()
        updated_mv.mv_title = new_movie
        db.session.commit()

    def delete_movie(self, movie_id):
        """Delete the movie with the given id."""
        del_mv = Movie.query.filter_by(mv_id=movie_id).first()
        db.session.delete(del_mv)
        db.session.commit()
