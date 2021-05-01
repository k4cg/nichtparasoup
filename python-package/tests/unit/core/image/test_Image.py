from typing import Any

import pytest

from nichtparasoup.core.image import Image


def test_uri_getter() -> None:
    # arrange
    image = Image(uri='url', source='src')
    # act
    uri = image.uri
    # assert
    assert 'url' == uri


def test_source_getter() -> None:
    # arrange
    image = Image(uri='url', source='src')
    # act
    src = image.source
    # assert
    assert 'src' == src


def test_generic_getter() -> None:
    # arrange
    image = Image(uri='url', source='src', is_generic=True)
    # act
    generic = image.is_generic
    # assert
    assert True is generic


def test_more_getter() -> None:
    # arrange
    image = Image(uri='url', source='src', some='more')
    # act
    more = image.more
    # assert
    assert {'some': 'more'} == more


@pytest.mark.parametrize(
    ('attr_name', 'attr_value'),
    [
        ('uri', 'foo'),
        ('source', 'foo'),
        ('is_generic', True),
        ('more', {})
    ],
    ids=[
        'uri',
        'source',
        'is_generic',
        'more',
    ]
)
def test_setter_throws(attr_name: str, attr_value: Any) -> None:
    # arrange
    image = Image(uri='url', source='src')
    # assert
    with pytest.raises(KeyError, match='frozen'):
        # act
        setattr(image, attr_name, attr_value)


@pytest.mark.parametrize(
    'attr_name',
    ['uri', 'source', 'is_generic', 'more']
)
def test_deleter_throws(attr_name: str) -> None:
    # arrange
    image = Image(uri='url', source='src')
    # assert
    with pytest.raises(KeyError, match='frozen'):
        # act
        delattr(image, attr_name)


def test_uri_causes_equality() -> None:
    # arrange
    image1 = Image(uri='url', source='src1', is_generic=False)
    image2 = Image(uri='url', source='src2', is_generic=False)
    # act
    equal = image1 == image2
    # assert
    assert True is equal


def test_uri_causes_same_hash() -> None:
    # arrange
    image1 = Image(uri='url', source='src1', is_generic=False)
    image2 = Image(uri='url', source='src2', is_generic=False)
    # act
    hash1 = hash(image1)
    hash2 = hash(image2)
    # assert
    assert hash1 == hash2


def test_generic_uri_causes_constant_hash() -> None:
    # arrange
    image = Image(uri='url', source='src1', is_generic=True)
    # act
    hash1 = hash(image)
    hash2 = hash(image)
    # assert
    assert hash1 == hash2


def test_generic_uri_causes_different_hash() -> None:
    # arrange
    image1 = Image(uri='url', source='src1', is_generic=True)
    image2 = Image(uri='url', source='src1', is_generic=True)
    # act
    hash1 = hash(image1)
    hash2 = hash(image2)
    # assert
    assert hash1 != hash2
