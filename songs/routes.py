from flask import Blueprint, make_response, jsonify, request
from auth.exceptions import AuthException
import songs.services as services
from flask import send_from_directory
import os
from songs.serilizers import SongSerializer
from auth.decorators import login_required

songs_bp = Blueprint('songs', __name__)

@songs_bp.route('/')
def get_all_songs():
    queryString = request.args.get('q', '')    
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)

    results = services.query_song(queryString, page=page, per_page=limit)
    print(results.__dict__)
    
    response = SongSerializer.serialize_list(results.items)

    return make_response(jsonify({
        'hasNext': page * results.per_page < results.total,
        'hasPrev': page > 1,
        'page': page,
        'limit': limit,
        'results': response}), 200)  


@songs_bp.route('/<int:id>')
def get_song_by_id(id):
    song = services.get_songs_by_id(id)
    
    response = SongSerializer.serialize(song)

    return make_response(jsonify(response), 200)

@songs_bp.route('/uploads')
@login_required
def get_song_by_user(user):        
    songs = services.get_songs_by_uploader(user.id)
    
    response = SongSerializer.serialize_list(songs)

    return make_response(jsonify({'results': response}), 200)  
        

@songs_bp.route('/', methods=['POST'])
@login_required
def create_song(user):
    data = request.form
    
    file_id = services.save_file(request.files.get('file'))
    
    try:
        song = services.create_song(
            title=data['title'],
            artist=data['artist'],
            album=data['album'],
            release_date=data['release_date'],
            file_id=file_id,
            user_id=user.id
        )

        response = SongSerializer.serialize(song)

        return make_response(jsonify(response), 201)   
    
    except:
        return make_response(jsonify({
            'message': 'All fields are required.'
        }), 400)   


@songs_bp.route('/<int:id>', methods=['PUT'])
@login_required
def update_song(user, id):
    data = request.form

    file_id = None
    if 'file' in request.files:
        if request.files['file']:
            file_id = services.save_file(request.files['file'])            
        

    try:
        song = services.update_song(
            id=id,
            title=data['title'],
            artist=data['artist'],
            album=data['album'],
            release_date=data['release_date'],
            file_id=file_id,  
            user_id=user.id     
        )

        response = SongSerializer.serialize(song)

        return make_response(jsonify(response), 200)
    
    except AuthException as e:
        return make_response(jsonify({'message': e.message}), 401)
    
    except:
        return make_response(jsonify({'message': 'All fields are requried.'}), 400)


@songs_bp.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_song(user, id):
    try:
        song = services.delete_song(id, user.id)
        response = SongSerializer.serialize(song)
        return make_response(jsonify(response), 200)
    except AuthException as e:
        return make_response(jsonify({'message': e.message}), 401)


@songs_bp.route('/<int:id>/file')
def get_song_file(id):
    song = services.get_songs_by_id(id)

    return send_from_directory(os.getenv('UPLOAD_FOLDER'), song.file.name)