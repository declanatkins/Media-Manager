from .abc import MediaItem


class Game(MediaItem):
    """Media Item representing a Game
    """

    def __init__(
            self,
            name: str,
            data_path: str,
            thumbnail_path: str,
            genres: str,
            platform: str,
            multiplayer: str
    ):
        super(Game).__init__(name, data_path, thumbnail_path, genres)

        self._multiplayer = multiplayer
        self._platform = platform
        
    def as_json(self) -> dict:
        return {
            '_id': self._id,
            'type': 'Game',
            'name': self._name,
            'thumbnail': self._thumbnail_path,
            'genres': self._genres,
            'multiplayer': self._multiplayer,
            'platform': self._platform,
            data_path: self._data_path
        }
