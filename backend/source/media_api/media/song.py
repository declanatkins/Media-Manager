from .abc import MediaItem


class Song(MediaItem):
    """Media Item representing a Song
    """

    def __init__(
            self,
            name: str,
            data_path: str,
            thumbnail_path: str,
            genres: str,
            artist: str,
            album: str
    ):
        super(Song).__init__(name, data_path, thumbnail_path, genres)

        self._artist = artist
        self._album = album
        
    def as_json(self) -> dict:
        return {
            '_id': self._id,
            'type': 'Movie',
            'name': self._name,
            'thumbnail': self._thumbnail_path,
            'genres': self._genres,
            'artist': self._artist,
            'album': self._album
        }
