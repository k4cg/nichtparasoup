from typing import Iterable, Tuple

import pytest

from nichtparasoup.core import NPCore
from nichtparasoup.core.server import BlacklistStatus, CrawlerStatus, Server, ServerStatus

from .._mocks.mockable_imagecrawler import MockableImageCrawler

_ImagecrawlersAndServer = Tuple[Iterable[Tuple[MockableImageCrawler, int]], Server]


@pytest.fixture(scope='module')
def imagecrawlers_and_server() -> _ImagecrawlersAndServer:
    # set up
    core = NPCore()
    imagecrawlers = ((MockableImageCrawler(t=1), 1), (MockableImageCrawler(t=2), 1))
    for (imagecrawler, weight) in imagecrawlers:
        core.add_imagecrawler(imagecrawler, weight=weight)
    server = Server(core)
    # issue test
    return imagecrawlers, server


@pytest.mark.skip(reason='test not written')
def test_server(imagecrawlers_and_server: _ImagecrawlersAndServer) -> None:
    # arrange
    imagecrawlers, server = imagecrawlers_and_server
    # act
    status = ServerStatus(server)
    # assert
    assert status  # TODO write the tests


@pytest.mark.skip(reason='test not written')
def test_blacklist(imagecrawlers_and_server: _ImagecrawlersAndServer) -> None:
    # arrange
    imagecrawlers, server = imagecrawlers_and_server
    # act
    status = BlacklistStatus(server)
    # assert
    assert status  # TODO write the tests


@pytest.mark.skip(reason='test not written')
def test_crawlers(imagecrawlers_and_server: _ImagecrawlersAndServer) -> None:
    # arrange
    imagecrawlers, server = imagecrawlers_and_server
    # act
    status = CrawlerStatus(server)
    # assert
    assert status  # TODO write the tests
