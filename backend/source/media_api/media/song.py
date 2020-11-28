from .abc import MediaItem


class Song(MediaItem):
    """Media Item representing a Song
    """

    def __init__(
            self,
            name: str,
            thumbnail_path: str,
            genres: str,
            artist: str,
            album: str, 
            id_=None
    ):
        super().__init__(name, thumbnail_path, genres, id_)

        self._artist = artist
        self._album = album
        
    def as_json(self) -> dict:
        return {
            '_id': self._id,
            'type': 'Song',
            'name': self._name,
            'thumbnail_path': self._thumbnail_path,
            'genres': self._genres,
            'artist': self._artist,
            'album': self._album
        }
