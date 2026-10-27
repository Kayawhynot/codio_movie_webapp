from models import db, User, Movie


class DataManager:
    def create_user(self, usr_name):
        new_user = User(name=usr_name)
        db.session.add(new_user)
        db.session.commit()

    def get_users(self):
        return User.query.all()

    def get_movies(self, user_srch_id):
        return Movie.query.filter_by(user_id=user_srch_id).all()

    def add_movie(self, movie_data):
        db.session.add(movie_data)
        db.session.commit()

    def update_movie(self, movie_id, new_movie):
        updated_mv = Movie.query.filter_by(mv_id=movie_id).first()
        updated_mv.mv_title = new_movie
        db.session.commit()

    def delete_movie(self, movie_id):
        del_mv = Movie.query.filter_by(mv_id=movie_id).first()
        db.session.delete(del_mv)
        db.session.commit()
