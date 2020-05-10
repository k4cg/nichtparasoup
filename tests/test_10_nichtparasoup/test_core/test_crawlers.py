from typing import List, Optional
from unittest.mock import MagicMock

import pytest  # type: ignore

from nichtparasoup.core import Crawler, CrawlerCollection, _CrawlerWeight

from .mockable_imagecrawler import MockableImageCrawler


class TestCrawlers:

    @pytest.mark.parametrize(  # type: ignore
        ('weights', 'weight_rnd', 'expected_choice'), [
            ([], 0, None), ([], 1, None),
            ([1], 0, 0), ([1], 0.5, 0), ([1], 1, 0),
            ([1, 2], 0, 0), ([0.7, 2], 0.5, 0), ([1, 2], 1.001, 1), ([1, 2], 3, 1)
        ], )
    def test_get_random(self, weights: List[_CrawlerWeight],
                        weight_rnd: _CrawlerWeight, expected_choice: Optional[int]
                        ) -> None:
        # arrange
        crawlers = CrawlerCollection()
        crawlers._random_weight = MagicMock(return_value=weight_rnd)  # type: ignore
        for weight in weights:
            crawlers.append(Crawler(MockableImageCrawler(), weight))
        # act
        random_crawler = crawlers.get_random()
        # assert
        if expected_choice is None:
            assert random_crawler is None, 'did not expect choice'
        else:
            assert random_crawler is crawlers[expected_choice], 'did expect different choice'
