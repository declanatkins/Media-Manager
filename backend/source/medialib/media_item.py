from abc import ABC
from abc import abstractmethod
from uuid import uuid4


class MediaItem(ABC):
    """Base class representing a media item
    """

    def __init__(self, name: str, thumbnail='', genres=[]):
        self._name = name
        self._thumbnail = thumbnail
        self._genres = genres
        self._id = uuid4()

    @abstractmethod
    def as_json(self) -> dict: 
        """Return a json representation of the media item
        """
        raise NotImplemented("Error - calling unimplemented abstract method")
