__all__ = ["Image", "ImageCollection", "ImageUri", "SourceUri"]

from typing import Any, Set, Union
from uuid import uuid4

from .._internals import _type_module_name_str

ImageUri = str

SourceUri = str


class Image:
    """Describe an image

    `uri`
        The absolute URI of the image. This basically identifies the Image and makes it unique.

        This absolute URI must include: ``scheme``, ``host``.
            ``scheme`` must be either 'http' or 'https' - use 'https' if possible!
        Optional are: ``port``, ``path``, ``query``, ``fragment``.

    `source`
        The URI where did the image is originally found?
        This URI can point to a ImageBoardThread, or a comment section in a Forum, or a news article...

        In the idea of fair use, it is encouraged to point to the source as good as possible.

        This absolute URI must include: ``scheme``, ``host``.
            ``scheme`` must be either 'http' or 'https' - the last one is preferred.
        Optional are: ``port``, ``path``, ``query``, ``fragment``.

        Good examples are:
            * https://www.reddit.com/r/Awww/comments/e1er0c/say_hi_to_loki_hes_just_contemplating/
            * https://giphy.com/gifs/10kABVanhwykJW

    `is_generic`
        If a generic image crawler is used, its common that each image URI looks exactly the same.
        To make this known, use this flag.

    `more`
        A dictionary of additional information an image crawler might want to deliver.

        This dictionary's data types are intended to the basic ones: string, int, float, list, set, dict, bool, None

        Good examples are:
            * image-dimensions
            * author, copyright information
            * valid-until

    """

    def __init__(self, *,
                 uri: ImageUri, source: SourceUri,
                 is_generic: bool = False,
                 **more: Any) -> None:  # pragma: no cover
        self.uri = uri
        self.source = source
        self.more = more
        self.is_generic = is_generic
        self.__hash = hash(uuid4() if self.is_generic else self.uri)

    def __hash__(self) -> int:
        return self.__hash

    def __eq__(self, other: Union['Image', Any]) -> bool:
        if type(other) is not type(self):
            return NotImplemented
        return hash(self) == hash(other)

    def __ne__(self, other: Union['Image', Any]) -> bool:
        if type(other) is not type(self):
            return NotImplemented
        return hash(self) != hash(other)

    def __repr__(self) -> str:  # pragma: no cover
        return f'<{_type_module_name_str(type(self))} object at {id(self):#x} {self.uri!r}>'

    def __str__(self) -> str:
        return self.uri


class ImageCollection(Set[Image]):
    ...
