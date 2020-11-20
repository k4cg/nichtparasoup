import sys
from random import randint, uniform as randfloat
from typing import Any, Callable, Union
from unittest.mock import Mock, PropertyMock, call, patch

import pytest

from nichtparasoup.core import Crawler as Sut
from nichtparasoup.core.image import Image, ImageCollection

if sys.version_info[:2] >= (3, 7):
    from contextlib import nullcontext as does_not_raise
else:
    from contextlib import contextmanager

    @contextmanager
    def does_not_raise() -> None:
        yield


@pytest.mark.parametrize(
    ('weight', 'expectation'),
    [
        (-randfloat(1.0, 99999.0), pytest.raises(ValueError, match='weight')),
        (0, pytest.raises(ValueError, match='weight')),
        (+randfloat(1.0, 99999.0), does_not_raise()),
    ],
    ids=[
        'negative',
        'zero',
        'positive',
    ]
)
def test_get_set_weight(weight: Union[int, float], expectation: Any) -> None:
    # arrange
    old_weight = Mock()
    sut = Mock(Sut, _weight=old_weight)
    assert Sut.get_weight(sut) is old_weight
    # act
    with expectation as ex:
        Sut.set_weight(sut, weight)
    new_weight = Sut.get_weight(sut)
    # assert
    if ex:
        assert new_weight is old_weight
    else:
        assert new_weight == weight


def __dummy_set_is_image_addable(_: Any) -> bool:
    raise NotImplementedError()


class __DummySetIsImageAddable:

    @staticmethod
    def sm(_: Any) -> bool:
        raise NotImplementedError()

    @classmethod
    def cm(cls, _: Any) -> bool:
        raise NotImplementedError()

    def im(self, _: Any) -> bool:
        raise NotImplementedError()


@pytest.mark.parametrize(
    'is_image_addable',
    [
        __DummySetIsImageAddable().im,
        __DummySetIsImageAddable.cm,
        __DummySetIsImageAddable.sm,
        __dummy_set_is_image_addable,
        lambda i: __dummy_set_is_image_addable(i),
    ],
    ids=[
        'InstanceMethod',
        'ClassMethod',
        'StaticMethod',
        'Function',
        'Lambda'
    ],
)
def test_get_set_is_image_addable(is_image_addable: Callable[[Any], bool]) -> None:
    # arrange
    old_is_image_addable = Mock()
    sut = Mock(Sut, _is_image_addable=old_is_image_addable)
    assert Sut.get_is_image_addable(sut) is old_is_image_addable
    # act
    Sut.set_is_image_addable(sut, is_image_addable)
    new_is_image_addable = Sut.get_is_image_addable(sut)
    # assert
    assert new_is_image_addable == is_image_addable


def test_get_del_is_image_addable() -> None:
    # arrange
    old_is_image_addable = Mock()
    sut = Mock(Sut, _is_image_addable=old_is_image_addable)
    assert Sut.get_is_image_addable(sut) is old_is_image_addable
    # act
    Sut.del_is_image_addable(sut)
    # assert
    assert Sut.get_is_image_addable(sut) is None


def __dummy_set_image_added(_: Any) -> None:
    raise NotImplementedError()


class __DummySetImageAdded:

    @staticmethod
    def sm(_: Any) -> None:
        raise NotImplementedError()

    @classmethod
    def cm(cls, _: Any) -> None:
        raise NotImplementedError()

    def im(self, _: Any) -> None:
        raise NotImplementedError()


@pytest.mark.parametrize(
    'image_added',
    [
        __DummySetImageAdded().im,
        __DummySetImageAdded.cm,
        __DummySetImageAdded.sm,
        __dummy_set_image_added,
        lambda i: __dummy_set_image_added(i)
    ],
    ids=[
        'InstanceMethod',
        'ClassMethod',
        'StaticMethod',
        'Function',
        'Lambda'
    ],
)
def test_get_set_image_added(image_added: Callable[[Any], None]) -> None:
    # arrange
    old_image_added = Mock()
    sut = Mock(Sut, _image_added=old_image_added)
    assert Sut.get_image_added(sut) is old_image_added
    # act
    Sut.set_image_added(sut, image_added)
    new_image_added = Sut.get_image_added(sut)
    # assert
    assert new_image_added == image_added


def test_get_del_image_added() -> None:
    # arrange
    old_image_added = Mock()
    sut = Mock(Sut, _image_added=old_image_added)
    assert Sut.get_image_added(sut) is old_image_added
    # act
    Sut.del_image_added(sut)
    # assert
    assert Sut.get_image_added(sut) is None


def test_reset() -> None:
    # arrange
    sut = Mock(Sut, images=Mock(), imagecrawler=Mock())
    # act
    Sut.reset(sut)
    # assert
    sut.images.clear.assert_called_once()
    sut.imagecrawler.reset.assert_called_once()


@pytest.mark.parametrize('is_exhausted', [True, False])
@pytest.mark.parametrize('restart_at_front_when_exhausted', [True, False])
def test_crawl(is_exhausted: bool, restart_at_front_when_exhausted: bool) -> None:
    # arrange
    images = {Mock() for _ in range(randint(0, 99))}
    sut = Mock(
        Sut,
        imagecrawler=Mock(
            is_exhausted=Mock(return_value=is_exhausted),
            crawl=Mock(return_value=images),
        ),
        restart_at_front_when_exhausted=restart_at_front_when_exhausted,
        _add_images=Mock(return_value=len(images)),
    )
    # act
    crawled = Sut.crawl(sut)
    # assert
    sut.imagecrawler.is_exhausted.assert_called_once()
    if is_exhausted:
        if restart_at_front_when_exhausted:
            sut.imagecrawler.reset.assert_called_once()
        else:
            sut.imagecrawler.reset.assert_not_called()
    if is_exhausted and not restart_at_front_when_exhausted:
        sut.imagecrawler.crawl.assert_not_called()
        assert crawled == 0
    else:
        sut.imagecrawler.crawl.assert_called_once()
        sut._add_images.assert_called_once_with(images)
        assert crawled == len(images)


def test__add_images() -> None:
    # arrange
    old_images = ImageCollection(Mock(Image, name=f'image{i}') for i in range(randint(0, 99)))
    invalid_images = ImageCollection(Mock(Image, name=f'image{i}') for i in range(randint(0, 99)))
    new_images = ImageCollection(Mock(Image, name=f'image{i}') for i in range(randint(0, 99)))
    image_added = Mock(callable, return_value=None)
    with patch.multiple(
        Sut,
        is_image_addable=PropertyMock(return_value=lambda image: image not in invalid_images),
        image_added=PropertyMock(return_value=image_added)
    ):
        sut = Sut(imagecrawler=Mock())
        sut.images = old_images.copy()
        # act
        added = Sut._add_images(sut, ImageCollection(invalid_images | new_images))
    # assert
    assert added == len(new_images)
    for image in old_images:
        assert image in sut.images
    for image in new_images:
        assert image in sut.images
        assert call(image) in image_added.call_args_list
    for image in invalid_images:
        assert image not in sut.images
        assert call(image) not in image_added.call_args_list
