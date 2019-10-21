__all__ = ["Image", "ImageCollection", "ImageSource", "ImageUri"]

from typing import Any, Optional, Set
from uuid import uuid4

ImageUri = str

ImageSource = str


class Image(object):

    def __init__(self, uri: ImageUri,
                 is_generic: bool = False, source: Optional[ImageSource] = None,
                 **more: Any) -> None:  # pragma: no cover
        self.uri = uri
        self.source = source
        self.more = more
        self.is_generic = is_generic
        self.__hash = hash(uuid4()) if self.is_generic else hash(self.uri)

    def __hash__(self) -> int:
        return self.__hash

    def __eq__(self, other: Any) -> bool:
        if type(other) is type(self):
            return hash(self) == hash(other)
        return False


class ImageCollection(Set[Image]):
    pass
