from .abc import MediaItem


class Movie(MediaItem):
    """Media Item representing a Movie
    """

    def __init__(
            self,
            name: str,
            thumbnail_path: str,
            genres: str,
            director: str,
            starring: str,
            id_=None
    ):
        super().__init__(name, thumbnail_path, genres, id_)

        self._director = director
        self._starring = starring

    def as_json(self) -> dict:
        return {
            '_id': self._id,
            'type': 'Movie',
            'name': self._name,
            'thumbnail_path': self._thumbnail_path,
            'genres': self._genres,
            'director': self._director,
            'starring': self._starring
        }
