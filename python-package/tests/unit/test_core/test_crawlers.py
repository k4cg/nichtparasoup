from nichtparasoup.core import CrawlerCollection


class TestCrawlers:

    def test_get_random_from_empty(self) -> None:
        # arrange
        crawlers = CrawlerCollection()
        # act
        random_crawler = crawlers.get_random()
        # assert
        assert random_crawler is None

    def test_copy(self) -> None:
        # arrange
        crawlers = CrawlerCollection()
        # act
        copy = crawlers.copy()
        # assert
        assert isinstance(copy, CrawlerCollection)
        assert copy is not crawlers
        assert copy == crawlers
