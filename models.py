from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A person who keeps a list of favourite movies."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class Movie(db.Model):
    """A movie saved for one user, with details from OMDb."""

    mv_id = db.Column(db.Integer, primary_key=True)
    mv_poster = db.Column(db.String, nullable=True)
    mv_title = db.Column(db.String(100), nullable=False)
    mv_director = db.Column(db.String(100), nullable=False)
    mv_release_yr = db.Column(db.String(4), nullable=False)
    mv_actor1 = db.Column(db.String(100), nullable=True)
    mv_actor2 = db.Column(db.String(100), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
