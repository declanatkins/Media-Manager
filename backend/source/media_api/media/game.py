from .abc import MediaItem


class Game(MediaItem):
    """Media Item representing a Game
    """

    def __init__(
            self,
            name: str,
            thumbnail_path: str,
            genres: str,
            platform: str,
            multiplayer: str,
            id_=None
    ):
        super().__init__(name, thumbnail_path, genres, id_)

        self._multiplayer = multiplayer
        self._platform = platform
        
    def as_json(self) -> dict:
        return {
            '_id': self._id,
            'type': 'Game',
            'name': self._name,
            'thumbnail_path': self._thumbnail_path,
            'genres': self._genres,
            'multiplayer': self._multiplayer,
            'platform': self._platform
        }
