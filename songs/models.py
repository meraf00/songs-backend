from auth.models import User
from db import db

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    artist = db.Column(db.String(50))
    album = db.Column(db.String(50))
    release_date = db.Column(db.String(50))
    file_id = db.Column(db.Integer, db.ForeignKey(File.id))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    file = db.relationship(File, foreign_keys=[file_id], cascade="all,delete")
    user = db.relationship(User, foreign_keys=[user_id])
