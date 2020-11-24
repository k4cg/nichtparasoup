from http.client import HTTPResponse
from unittest.mock import Mock

from nichtparasoup.imagecrawler import RemoteFetcher as Sut


def test_get_stream() -> None:
    pass


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
    assert got_url == actual_url
    assert got_bytes == actual_bytes
    actual_response.close.assert_called_once()


def test_get_string() -> None:
    # arrange
    actual_url = 'actual_url'
    actual_string = 'actual_string'
    actual_encoding = 'ascii'
    actual_response_info = {'charset': actual_encoding}
    actual_response = Mock(HTTPResponse)
    actual_response.read.return_value = actual_string.encode(actual_encoding)
    actual_response.info.return_value.get_param.side_effect = actual_response_info.get
    sut = Mock(Sut)
    sut.get_stream.return_value = actual_response, actual_url
    # act
    got_string, got_url = Sut.get_string(sut, 'url')
    # assert
    assert got_url == actual_url
    assert got_string == actual_string
    actual_response.close.assert_called_once()
