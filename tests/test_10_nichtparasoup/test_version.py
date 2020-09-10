import unittest


class VersionTest(unittest.TestCase):

    def test_version_known(self) -> None:
        # arrange
        from nichtparasoup import VERSION  # isort:skip
        # assert
        self.assertFalse(
            VERSION.startswith('UNKNOWN'),
            'unknown version: {!r}'.format(VERSION)
        )
