from nichtparasoup.imagecrawler import ImageCrawler, Images


class _EmptyImageCrawler(ImageCrawler):
    """ imagecrawler that finds nothing. use it for mocking ... """

    def crawl(self) -> Images:
        return Images()
