from abc import ABC
from abc import abstractmethod
from uuid import uuid4


class MediaItem(ABC):
    """Base class representing a media item

    Args:
        name (str): name of the media item
        data_path (str): path to the data for this media item
        thumbnail_path (str): path to the thumbnail for this media item
        genres (list[str]): list of genres for this media item
    """

    def __init__(self, name: str, thumbnail_path='', genres=[], id_=None):
        self._name = name
        self._thumbnail_path = thumbnail_path
        self._genres = genres
        self._id = id_ or str(uuid4())

    @property
    def id_code(self) -> str:
        return self._id

    @abstractmethod
    def as_json(self) -> dict:
        """Return a json representation of the media item
        """
        raise NotImplementedError("Error - calling unimplemented abstract method")
