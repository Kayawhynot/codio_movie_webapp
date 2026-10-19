from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Movie(db.Model):
    mv_id = db.Column(db.Integer, primary_key=True)
    mv_title = db.Column(db.Integer, nullable=False)
    mv_release_yr = db.Column(db.String(4), nullable=False)
    mv_actor1 = db.Column(db.String(100), nullable=True)
    mv_actor2 = db.Column(db.String(100), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_id'), nullable=False)