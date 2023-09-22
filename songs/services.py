from auth.exceptions import AuthException
from db import db
import os
from songs.models import File, Song
from werkzeug.utils import secure_filename


def get_all_songs(page=1, per_page=10):
    page = Song.query.paginate(page=page, per_page=per_page)

    return page.items


def get_songs_by_id(id):
    song = Song.query.filter_by(id=id).first()

    return song

def get_songs_by_uploader(user_id, page=1, per_page=10):
    page = Song.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page)

    return page.items

def query_song(queryString, page=1, per_page=10):
    results = Song.query.filter(
        Song.title.like(f'%{queryString}%') | 
        Song.artist.like(f'%{queryString}%') | 
        Song.album.like(f'%{queryString}%') | 
        Song.release_date.like(f'%{queryString}%')
    ).paginate(page=page, per_page=per_page)    

    return results.items

def create_song(title, artist, album, release_date, file_id, user_id):
    song = Song(
        title=title,
        artist=artist,
        album=album,
        release_date=release_date,
        file_id=file_id,
        user_id=user_id
    )

    db.session.add(song)
    db.session.commit()

    return song

def update_song(id, title, artist, album, release_date, file_id, user_id):
    song = Song.query.filter_by(id=id).first()

    if song.user.id != user_id:
        raise AuthException('You are not authorized to update this song')

    song.title = title
    song.artist = artist
    song.album = album
    song.release_date = release_date
    
    if file_id:
        song.file_id = file_id

    db.session.commit()

    return song

def delete_song(id, user_id):
    song = Song.query.filter_by(id=id).first()

    if song.user.id != user_id:
        raise AuthException('You are not authorized to update this song')
    
    os.remove(song.file.path)    

    db.session.delete(song)
    db.session.commit()

    return song


def save_file(file):    
    filename = secure_filename(file.filename)    
    path = os.path.join(os.getenv('UPLOAD_FOLDER'), filename)    
    file.save(path)

    file = File(name=filename)
    
    db.session.add(file)
    db.session.commit()

    return file.id