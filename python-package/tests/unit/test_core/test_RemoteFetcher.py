import os
from http.client import HTTPResponse
from io import BytesIO
from random import choice, randint, uniform as randfloat
from unittest.mock import Mock

import pytest
from py.path import local as LocalPath  # noqa: N812
from pytest_mock import MockerFixture

from nichtparasoup.core.imagecrawler import RemoteFetcher as Sut, RemoteFetchError


def test_get_stream(mocker: MockerFixture) -> None:
    # arrange
    mocker.patch.dict(os.environ, {Sut.ENV_STOREDIR: ''})
    actual_url = 'actual_url'
    actual_response = Mock(HTTPResponse, name='actual_response')
    actual_response.geturl.return_value = actual_url
    timeout = randfloat(1.0, 9.9)
    headers = {'x-foo': 'foo', 'x-bar': 'bazz'}
    sut = Sut(timeout=timeout, headers=headers)
    valid_uri = mocker.patch.object(Sut, '_valid_uri', return_value=True)
    request_url = 'request_url'
    debug_write_response = mocker.patch.object(sut, '_debug_write_response')
    urlopen = mocker.patch('nichtparasoup.core.imagecrawler.urlopen', return_value=actual_response)
    request = mocker.patch('nichtparasoup.core.imagecrawler.Request')
    # act
    got_response, got_url = Sut.get_stream(sut, request_url)
    # assert
    valid_uri.assert_called_with(request_url)
    request.assert_called_once()
    assert request.call_args.args[0] == request_url
    for header_name, header_value in headers.items():
        assert request.call_args.kwargs['headers'][header_name] == header_value
    urlopen.call_args(request.return_value, timeout=timeout)
    debug_write_response.assert_called_once_with(actual_response, request_url)
    assert got_response == actual_response
    assert got_url == actual_url


def test_get_stream_invalid_url(mocker: MockerFixture) -> None:
    # arrange
    sut = Mock()
    sut._valid_uri.return_value = False
    request_url = 'request_url'
    urlopen = mocker.patch('nichtparasoup.core.imagecrawler.urlopen')
    # act
    with pytest.raises(ValueError, match=request_url):
        Sut.get_stream(sut, request_url)
    # assert
    urlopen.assert_not_called()


def test_get_stream_broken_fetch(mocker: MockerFixture) -> None:
    # arrange
    sut = Mock()
    sut._valid_uri.return_value = True
    mocker.patch('nichtparasoup.core.imagecrawler.urlopen', side_effect=Exception())
    mocker.patch('nichtparasoup.core.imagecrawler.Request')
    # assert
    with pytest.raises(RemoteFetchError):
        # act
        Sut.get_stream(sut, 'foo')


def test_get_bytes() -> None:
    # arrange
    actual_url = 'actual_url'
    actual_bytes = b'actual_bytes'
    actual_response = Mock(HTTPResponse)
    actual_response.read.return_value = actual_bytes
    sut = Mock(Sut)
    sut.get_stream.return_value = actual_response, actual_url
    # act
    got_bytes, got_url = Sut.get_bytes(sut, 'url')
    # assert
    assert got_bytes == actual_bytes
    assert got_url == actual_url
    actual_response.close.assert_called_once()


def test_get_string() -> None:
    # arrange
    actual_url = 'actual_url'
    actual_string = 'actual_string'
    actual_encoding = choice(['ASCII', 'UTF-8', 'Latin-1', 'ISO 8859-1', 'Windows-1252'])
    actual_response_info = {'charset': actual_encoding}
    actual_response = Mock(HTTPResponse)
    actual_response.read.return_value = actual_string.encode(actual_encoding)
    actual_response.info.return_value.get_param.side_effect = actual_response_info.get
    sut = Mock(Sut)
    sut.get_stream.return_value = actual_response, actual_url
    # act
    got_string, got_url = Sut.get_string(sut, 'url')
    # assert
    assert got_string == actual_string
    assert got_url == actual_url
    actual_response.close.assert_called_once()


@pytest.mark.parametrize(
    ('uri', 'expected_valid'),
    [
        ('http://test.url', True),
        ('https://test.url', True),
        ('file://test.url', False),
        ('ftp://test.url', False),
        ('test.url', False),
    ],
    ids=[
        'http',
        'https',
        'file',
        'ftp',
        'none',
    ]
)
def test__valid_uri(uri: str, expected_valid: bool) -> None:
    # act
    got_valid = Sut._valid_uri(uri)
    # assert
    assert got_valid is expected_valid


def test_store_for_debbug(mocker: MockerFixture, tmpdir: LocalPath) -> None:
    # arrange
    mocker.patch.dict(os.environ, {Sut.ENV_STOREDIR: tmpdir.strpath})
    request_url = 'request_url'
    response_data = bytes(randint(0, 7) for _ in range(randint(256, 1024)))
    response = Mock(HTTPResponse, fp=BytesIO(response_data))
    response.geturl.return_value = request_url
    response.getheaders.return_value = {'x-foo': 'foo', 'x-bar': 'bar'}.items()
    # act
    sut = Sut()
    sut._debug_write_response(response, request_url)
    # assert
    assert response.fp.read() == response_data
    tempfile = tmpdir.listdir()[0]
    assert tempfile.isfile()
    assert response_data in tempfile.open(mode='rb').read()
