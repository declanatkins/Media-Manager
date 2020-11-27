from .abc import MediaItem


class Movie(MediaItem):
    """Media Item representing a Movie
    """

    def __init__(
            self,
            name: str,
            data_path: str,
            thumbnail_path: str,
            genres: str,
            director: str,
            starring: str
    ):
        super(Movie).__init__(name, data_path, thumbnail_path, genres)

        self._director = director
        self._starring = starring
        
    def as_json(self) -> dict:
        return {
            '_id': self._id,
            'type': 'Movie',
            'name': self._name,
            'thumbnail': self._thumbnail_path,
            'genres': self._genres,
            'director': self._director,
            'starring': self._starring,
            'data_path': self._data_path
        }
