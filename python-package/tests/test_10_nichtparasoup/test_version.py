import unittest


class VersionTest(unittest.TestCase):

    def test_version_known(self) -> None:
        # arrange
        from nichtparasoup import __version__
        # assert
        self.assertFalse(
            __version__.startswith('UNKNOWN'),
            'unknown version: {!r}'.format(__version__)
        )
