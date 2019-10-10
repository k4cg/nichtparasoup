import unittest
from unittest.mock import MagicMock
from ddt import ddt, data as ddt_data, unpack as ddt_unpack  # type: ignore

from typing import List, Optional

from nichtparasoup.nichtparasoup import Crawler, Crawlers, CrawlerWeight

from . import _EmptyImageCrawler


@ddt
class CrawlersTest(unittest.TestCase):

    @ddt_data(  # type: ignore
        ([], 0, None), ([], 1, None),
        ([1], 0, 0), ([1], 0.5, 0), ([1], 1, 0),
        ([1, 2], 0, 0), ([0.7, 2], 0.5, 0), ([1, 2], 1.001, 1), ([1, 2], 3, 1),
    )
    @ddt_unpack  # type: ignore
    def test_get_random(self, weights: List[CrawlerWeight],
                        weight_rnd: CrawlerWeight, expected_choice: Optional[int]
                        ) -> None:
        # arrange
        crawlers = Crawlers()
        crawlers._random_weight = MagicMock(return_value=weight_rnd)  # type: ignore
        for weight in weights:
            crawlers.append(Crawler(_EmptyImageCrawler('test'), weight))

        # act
        random_crawler = crawlers.get_random()

        # assert
        if expected_choice is None:
            self.assertIsNone(random_crawler, "did not expect choice")
        else:
            self.assertIs(random_crawler, crawlers[expected_choice], "did expect different coice")
