import pytest

from nichtparasoup.core.image import Image

__parametrize_is_generic = {
    'argnames': 'is_generic',
    'argvalues': [False, True],
    'ids': ['non-generic', 'generic'],
}


@pytest.mark.parametrize(**__parametrize_is_generic)
def test_eq(is_generic: bool) -> None:
    # arrange
    image1 = Image(is_generic=is_generic, uri='test', source='test1')
    image2 = Image(is_generic=is_generic, uri='test', source='test2')
    # act
    eq = image1 == image1
    eq12 = image1 == image2
    eq21 = image2 == image1
    # assert
    assert eq
    assert is_generic != eq12
    assert is_generic != eq21


@pytest.mark.parametrize(**__parametrize_is_generic)
def test_ne(is_generic: bool) -> None:
    # arrange
    image1 = Image(is_generic=is_generic, uri='test', source='test1')
    image2 = Image(is_generic=is_generic, uri='test', source='test2')
    # act
    ne = image1 != image1
    ne12 = image1 != image2
    ne21 = image2 != image1
    # assert
    assert not ne
    assert is_generic == ne12
    assert is_generic == ne21


@pytest.mark.parametrize(**__parametrize_is_generic)
def test_hash(is_generic: bool) -> None:
    # arrange
    image1 = Image(is_generic=is_generic, uri='test', source='test1')
    image2 = Image(is_generic=is_generic, uri='test', source='test2')
    # act
    hash1 = hash(image1)
    hash2 = hash(image2)
    hash_eq = hash1 == hash2
    # assert
    assert is_generic != hash_eq


@pytest.mark.parametrize(**__parametrize_is_generic)
def test_in_set(is_generic: bool) -> None:
    # arrange
    image1 = Image(is_generic=is_generic, uri='test', source='test1')
    image2 = Image(is_generic=is_generic, uri='test', source='test2')
    images = {image1, image2}
    # act
    in_set1 = image1 in images
    in_set2 = image2 in images
    # assert
    assert len(images) == (2 if is_generic else 1)
    assert in_set1
    assert in_set2


@pytest.mark.parametrize(**__parametrize_is_generic)
def test_delete_in_set(is_generic: bool) -> None:
    # arrange
    image1 = Image(is_generic=is_generic, uri='test', source='test1')
    image2 = Image(is_generic=is_generic, uri='test', source='test2')
    images = {image1, image2}
    assert len(images) == (2 if is_generic else 1)
    # act
    images.remove(image1)
    # assert
    assert len(images) == (1 if is_generic else 0)
