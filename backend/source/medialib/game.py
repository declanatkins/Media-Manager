from .media_item import MediaItem


DEFAULT_GAME_THUMBNAIL = 'game_default_img.png'


class Game(MediaItem):
    """Media Item representing a Game
    """

    def __init__(
            self,
            name: str,
            thumbnail: str,
            genres: str,
            platform: str,
            multiplayer: str
    ):
        super(Game).__init__(
            name=name,
            thumnail=thumbnail or DEFAULT_GAME_THUMBNAIL,
            genres=genres
        )

        self._multiplayer = multiplayer
        self._platform = platform
        
    def as_json(self) -> dict:
        return {
            'id': self._id,
            'name': self._name,
            'thumbnail': self._thumbnail,
            'genres': self._genres,
            'multiplayer': self._multiplayer,
            'platform': self._platform
        }
