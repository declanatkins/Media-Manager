from .abc import MediaItem


class Game(MediaItem):
    """Media Item representing a Game
    """

    def __init__(
            self,
            name: str,
            data: str,
            thumbnail: str,
            genres: str,
            platform: str,
            multiplayer: str
    ):
        super(Game).__init__(name, thumbnail, genres)

        self._multiplayer = multiplayer
        self._platform = platform
        
    def as_json(self) -> dict:
        return {
            '_id': self._id,
            'name': self._name,
            'thumbnail': self._thumbnail,
            'genres': self._genres,
            'multiplayer': self._multiplayer,
            'platform': self._platform
        }
