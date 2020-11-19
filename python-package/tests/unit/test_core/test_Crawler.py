import sys
from random import uniform as randfloat
from typing import Any, Callable, Union
from unittest.mock import Mock

import pytest

from nichtparasoup.core import Crawler as Sut

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
    ('is_image_addable', 'expectation'),
    [
        (__DummySetIsImageAddable().im, does_not_raise()),
        (__DummySetIsImageAddable.cm, does_not_raise()),
        (__DummySetIsImageAddable.sm, pytest.raises(NotImplementedError)),  # not implemented, yet
        (__dummy_set_is_image_addable, pytest.raises(NotImplementedError)),  # not implemented, yet
        (lambda i: __dummy_set_is_image_addable(i), pytest.raises(NotImplementedError)),  # not implemented, yet
    ],
    ids=[
        'InstanceMethod',
        'ClassMethod',
        'StaticMethod',
        'Function',
        'Lambda'
    ],
)
def test_get_set_is_image_addable(is_image_addable: Callable[[Any], bool], expectation: Any) -> None:
    # arrange
    old_is_image_addable = Mock()
    sut = Mock(Sut, _is_image_addable_wr=lambda: old_is_image_addable)
    assert Sut.get_is_image_addable(sut) is old_is_image_addable
    # act
    with expectation as ex:
        Sut.set_is_image_addable(sut, is_image_addable)
    new_is_image_addable = Sut.get_is_image_addable(sut)
    # assert
    if ex:
        assert new_is_image_addable is old_is_image_addable
    else:
        assert new_is_image_addable == is_image_addable


def test_get_del_is_image_addable() -> None:
    # arrange
    sut = Mock(Sut, _is_image_addable_wr=Mock())
    assert Sut.get_is_image_addable(sut) is not None
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
    ('image_added', 'expectation'),
    [
        (__DummySetImageAdded().im, does_not_raise()),
        (__DummySetImageAdded.cm, does_not_raise()),
        (__DummySetImageAdded.sm, pytest.raises(NotImplementedError)),  # not implemented, yet
        (__dummy_set_image_added, pytest.raises(NotImplementedError)),  # not implemented, yet
        (lambda i: __dummy_set_image_added(i), pytest.raises(NotImplementedError)),  # not implemented, yet
    ],
    ids=[
        'InstanceMethod',
        'ClassMethod',
        'StaticMethod',
        'Function',
        'Lambda'
    ],
)
def test_get_set_image_added(image_added: Callable[[Any], None], expectation: Any) -> None:
    # arrange
    old_image_added = Mock()
    sut = Mock(Sut, _image_added_wr=lambda: old_image_added)
    assert Sut.get_image_added(sut) is old_image_added
    # act
    with expectation as ex:
        Sut.set_image_added(sut, image_added)
    new_image_added = Sut.get_image_added(sut)
    # assert
    if ex:
        assert new_image_added is old_image_added
    else:
        assert new_image_added == image_added


def test_get_del_image_added() -> None:
    # arrange
    sut = Mock(Sut, _image_added_wr=Mock())
    assert Sut.get_image_added(sut) is not None
    # act
    Sut.del_image_added(sut)
    # assert
    assert Sut.get_image_added(sut) is None
