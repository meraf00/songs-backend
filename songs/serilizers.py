from flask import url_for

class SongSerializer:    
    @staticmethod
    def serialize(song) -> dict:
        return {
            'id': song.id,
            'title': song.title,
            'artist': song.artist,
            'album': song.album,
            'release_date': song.release_date,            
            'file': url_for('songs.get_song_file', id=song.id, _external=True ),
        }
    
    @staticmethod
    def serialize_list(songs) -> list[dict]:
        return list(map(SongSerializer.serialize, songs))