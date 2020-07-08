from typing import List
from weakref import ref as weak_ref

import pytest

from nichtparasoup.core import Crawler
from nichtparasoup.core.image import Image, ImageCollection

from .._mocks.mockable_imagecrawler import MockableImageCrawler


class _C(object):

    def m_b(self, _: Image) -> bool:
        return True

    def m(self, _: Image) -> None:
        pass


def _f_b(_: Image) -> bool:
    return True


def _f(_: Image) -> None:
    pass


class TestCrawlerIsImageAddable:
    """Test if the weakref is working as expected
    """

    def test_default(self) -> None:
        # arrange
        self.crawler = Crawler(MockableImageCrawler())
        # assert
        assert None is self.crawler.get_is_image_addable()

    def test_none(self) -> None:
        # arrange
        self.crawler = Crawler(MockableImageCrawler())
        obj = _C()
        self.crawler.set_is_image_addable(obj.m_b)
        # act
        self.crawler.set_is_image_addable(None)
        # assert
        assert None is self.crawler.get_is_image_addable()

    def test_object_bound_method_stay(self) -> None:
        # arrange
        self.crawler = Crawler(MockableImageCrawler())
        obj = _C()
        # act
        self.crawler.set_is_image_addable(obj.m_b)
        # assert
        assert obj.m_b == self.crawler.get_is_image_addable()

    def test_object_bound_method_lambda(self) -> None:
        # arrange
        self.crawler = Crawler(MockableImageCrawler())
        obj = _C()
        self.crawler.set_is_image_addable(obj.m_b)
        # act
        self.crawler.set_is_image_addable(_C().m_b)
        # assert
        assert None is self.crawler.get_is_image_addable()

    def test_object_bound_method_deleted(self) -> None:
        # arrange
        self.crawler = Crawler(MockableImageCrawler())
        obj = _C()
        obj_wr = weak_ref(obj)
        # act
        self.crawler.set_is_image_addable(obj.m_b)
        assert obj.m_b == self.crawler.get_is_image_addable()
        del obj
        # assert
        assert None is obj_wr(), 'obj is intended to be deleted'
        assert None is self.crawler.get_is_image_addable()

    def test_function(self) -> None:
        # Remember: FunctionType is LambdaType
        # arrange
        self.crawler = Crawler(MockableImageCrawler())
        # assert
        with pytest.raises(Exception):
            # currently not supporting `function`. write the test, when writing it is supported
            self.crawler.set_is_image_addable(_f_b)


class TestCrawlerImageAdded:
    """Test if the weakref is working as expected
    """

    def test_default(self) -> None:
        # arrange
        self.crawler = Crawler(MockableImageCrawler())
        # assert
        assert None is self.crawler.get_image_added()

    def test_none(self) -> None:
        # arrange
        self.crawler = Crawler(MockableImageCrawler())
        obj = _C()
        self.crawler.set_image_added(obj.m)
        # act
        self.crawler.set_image_added(None)
        # assert
        assert None is self.crawler.get_image_added()

    def test_object_bound_method_stay(self) -> None:
        # arrange
        self.crawler = Crawler(MockableImageCrawler())
        obj = _C()
        # act
        self.crawler.set_image_added(obj.m)
        # assert
        assert obj.m == self.crawler.get_image_added()

    def test_object_bound_method_lambda(self) -> None:
        # arrange
        self.crawler = Crawler(MockableImageCrawler())
        obj = _C()
        self.crawler.set_image_added(obj.m)
        # act
        self.crawler.set_image_added(_C().m)
        # assert
        assert None is self.crawler.get_image_added()

    def test_object_bound_method_deleted(self) -> None:
        # arrange
        self.crawler = Crawler(MockableImageCrawler())
        obj = _C()
        obj_wr = weak_ref(obj)
        # act
        self.crawler.set_image_added(obj.m)
        assert obj.m == self.crawler.get_image_added()
        del obj
        # assert
        assert None is obj_wr(), 'obj is intended to be deleted'
        assert None is self.crawler.get_image_added()

    def test_function(self) -> None:
        # Remember: FunctionType is LambdaType
        # arrange
        self.crawler = Crawler(MockableImageCrawler())
        # assert
        with pytest.raises(Exception):
            # currently not supporting `function`. write the test, when writing it is supported
            self.crawler.set_image_added(_f)


class TestCrawlerAddImages:

    def test_crawl_default(self) -> None:
        # arrange
        images = ImageCollection({Image(uri='1', source='test1'), Image(uri='2', source='test2')})
        crawler = Crawler(MockableImageCrawler())
        # act
        crawled = crawler._add_images(images)
        # assert
        assert images == crawler.images
        assert len(images) == crawled

    def test_crawl_is_addable_called(self) -> None:
        # arrange
        called_is_image_addable_with = ImageCollection()

        def on_is_addable_true(image: Image) -> bool:
            called_is_image_addable_with.add(image)
            return True

        images = ImageCollection({Image(uri='1', source='test1'), Image(uri='2', source='test2')})
        crawler = Crawler(MockableImageCrawler())
        crawler.get_is_image_addable = lambda: on_is_addable_true  # type: ignore[assignment]
        # act
        crawled = crawler._add_images(images)
        # assert
        assert images == called_is_image_addable_with
        assert len(images) == crawled

    def test_crawl_image_added_called(self) -> None:
        # arrange
        called_image_added_with = ImageCollection()

        def on_get_image_added(image: Image) -> None:
            called_image_added_with.add(image)

        images = ImageCollection({Image(uri='1', source='test1'), Image(uri='2', source='test2')})
        crawler = Crawler(MockableImageCrawler())
        crawler.get_image_added = lambda: on_get_image_added  # type: ignore[assignment]
        # act
        crawled = crawler._add_images(images)
        # assert
        assert images == called_image_added_with
        assert len(images) == crawled

    def test_add_needed(self) -> None:
        # arrange
        called_is_image_addable_with = ImageCollection()
        called_image_added_with = ImageCollection()

        addable_images = ImageCollection({Image(uri='1', source='test1'), Image(uri='2', source='test2')})
        forbidden_images = ImageCollection({Image(uri='3', source='test3'), Image(uri='4', source='test4')})
        images = ImageCollection(addable_images | forbidden_images)

        def on_is_addable_fake(image: Image) -> bool:
            called_is_image_addable_with.add(image)
            return image in addable_images

        def on_get_image_added(image: Image) -> None:
            called_image_added_with.add(image)

        crawler = Crawler(MockableImageCrawler())
        crawler.get_is_image_addable = lambda: on_is_addable_fake  # type: ignore[assignment]
        crawler.get_image_added = lambda: on_get_image_added  # type: ignore[assignment]
        # act
        crawled = crawler._add_images(images)
        # assert
        assert images == called_is_image_addable_with
        assert addable_images == called_image_added_with
        assert len(addable_images) == crawled


class TestCrawlerExhaustedCrawling:

    @pytest.mark.parametrize(
        ('restart', 'exhausted', 'expected_did_call_reset', 'expected_did_call_crawl'),
        [
            (False, False, [], [True]),
            (False, True, [], []),
            (True, False, [], [True]),
            (True, True, [True], [True]),
        ],
        ids=[
            'not-restart, not-exhausted',
            'not-restart, exhausted',
            'restart, not-exhausted',
            'restart, exhausted',
        ]
    )
    def test_crawl_exhausted_reset(self, restart: bool, exhausted: bool,
                                   expected_did_call_reset: List[bool],
                                   expected_did_call_crawl: List[bool]
                                   ) -> None:
        # arrange
        crawler = Crawler(MockableImageCrawler())
        did_call_reset = []
        did_call_crawl = []

        def fake_exhausted() -> bool:
            return exhausted

        def fake_reset() -> None:
            did_call_reset.append(True)

        def fake_crawl() -> ImageCollection:
            did_call_crawl.append(True)
            return ImageCollection()

        crawler.restart_at_front_when_exhausted = restart
        crawler.imagecrawler.is_exhausted = fake_exhausted  # type: ignore[assignment]
        crawler.imagecrawler.reset = fake_reset  # type: ignore[assignment]
        crawler.imagecrawler.crawl = fake_crawl  # type: ignore[assignment]
        # act
        crawler.crawl()
        # assert
        assert expected_did_call_reset == did_call_reset
        assert expected_did_call_crawl == did_call_crawl


class TestServerRefill:

    @pytest.mark.skip(reason="TODO: write the test - use Random3Crawler")
    def test_fill_up_to(self) -> None:
        raise NotImplementedError()

    @pytest.mark.skip(reason="TODO: write the test - use NullCrawler")
    def test_refill_null_crawler(self) -> None:
        raise NotImplementedError()
