__all__ = ["Image", "ImageCollection", "ImageUri", "SourceUri"]

from typing import Any, Dict, Set, Union
from uuid import uuid4

from .._internals import _type_module_name_str

ImageUri = str

SourceUri = str


class Image:
    # TODO when py >= (3.7) -- make this a data class, a frozen one.
    """Describe an image.

    An object is intended as immutable(frozen), to allow hashing without side effects.

    `uri`
        The absolute URI of the image. This basically identifies the Image and makes it unique.

        This absolute URI must include: ``scheme``, ``host``.
            ``scheme`` should be either 'http' or 'https' - use 'https' if possible!
        Optional are: ``port``, ``path``, ``query``, ``fragment``.

    `source`
        The URI where did the image is originally found?
        This URI can point to a ImageBoardThread, or a comment section in a Forum, or a news article...

        In the idea of fair use, it is encouraged to point to the source as good as possible.

        This absolute URI must include: ``scheme``, ``host``.
            ``scheme`` should be either 'http' or 'https' - the last one is preferred.
        Optional are: ``port``, ``path``, ``query``, ``fragment``.

        Good examples are:
            * https://www.reddit.com/r/Awww/comments/e1er0c/say_hi_to_loki_hes_just_contemplating/
            * https://giphy.com/gifs/10kABVanhwykJW

    `is_generic`
        If a generic image crawler is used, its common that each image URI looks exactly the same.
        To make this known, use this flag.
        This will also impact comparisons with ``==``, ``!=`` and hashes of the instance.
        A generic instance will never equal any other instance but itself.
        This is used to allow the "same" generic to exist multiple times in a ``set`` or ``ImageCollection``.

    `more`
        A dictionary of additional information an image crawler might want to deliver.

        This dictionary's data types are intended to the basic ones: string, int, float, list, set, dict, bool, None

        Good examples are:
            * image-dimensions
            * author, copyright information
            * valid-until

    """

    uri: ImageUri
    is_generic: bool
    source: SourceUri
    more: Dict[str, Any]
    __hash: int

    def __init__(self, *,
                 uri: ImageUri, source: SourceUri,
                 is_generic: bool = False,
                 **more: Any) -> None:
        super().__setattr__('uri', uri)
        super().__setattr__('is_generic', is_generic)
        super().__setattr__('source', source)
        super().__setattr__('more', more)
        super().__setattr__('_Image__hash', self.__gen_hash())

    def __setattr__(self, *_: Any, **__: Any) -> None:
        raise KeyError('object is frozen')

    def __delattr__(self, *_: Any, **__: Any) -> None:
        raise KeyError('object is frozen')

    def __gen_hash(self) -> int:
        return hash(uuid4() if self.is_generic else self.uri)

    def __hash__(self) -> int:
        return self.__hash

    def __eq__(self, other: Union['Image', Any]) -> bool:
        if isinstance(other, Image):
            return self.__hash == other.__hash
        return NotImplemented   # pragma: no cover

    def __repr__(self) -> str:  # pragma: no cover
        return f'<{_type_module_name_str(type(self))} object at {id(self):#x} {self.uri!r}>'

    def __str__(self) -> str:  # pragma: no cover
        return self.uri


class ImageCollection(Set[Image]):
    def copy(self) -> 'ImageCollection':
        return ImageCollection(super().copy())
