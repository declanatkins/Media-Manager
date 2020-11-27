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

    def __init__(self, name: str, data_path: str, thumbnail_path='', genres=[]):
        self._name = name
        self._thumbnail_path = thumbnail_path
        self._genres = genres
        self._data_path = data_path
        self._id = uuid4()

    @property
    def id_code(self) -> str:
        return self._id
    
    @abstractmethod
    def as_json(self) -> dict: 
        """Return a json representation of the media item
        """
        raise NotImplemented("Error - calling unimplemented abstract method")
