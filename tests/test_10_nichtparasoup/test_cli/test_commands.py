import unittest

from nichtparasoup.cli.commands import Commands


class CommandsRunTest(unittest.TestCase):

    @unittest.skip("TODO: write the test")
    def test_(self) -> None:
        raise NotImplementedError()


class CommandsConfigTest(unittest.TestCase):

    @unittest.skip("TODO: write the test")
    def test_(self) -> None:
        raise NotImplementedError()


class CommandsConfigDumpFileTest(unittest.TestCase):

    @unittest.skip("TODO: write the test")
    def test_(self) -> None:
        raise NotImplementedError()


class CommandsConfigCheckFileTest(unittest.TestCase):

    @unittest.skip("TODO: write the test")
    def test_(self) -> None:
        raise NotImplementedError()


class CommandsInfoTest(unittest.TestCase):

    @unittest.skip("TODO: write the test")
    def test_(self) -> None:
        raise NotImplementedError()


class CommandsInfoVersionTest(unittest.TestCase):

    def test_version(self) -> None:
        # TODO catch stdout and check against current nichtparasoup.VERSION
        ret = Commands.info_version()
        self.assertEqual(0, ret)


class CommandsInfoImagecrawlerListTest(unittest.TestCase):

    @unittest.skip("TODO: write the test")
    def test_(self) -> None:
        raise NotImplementedError()


class CommandsInfoImagecrawlerDescTest(unittest.TestCase):

    @unittest.skip("TODO: write the test")
    def test_(self) -> None:
        raise NotImplementedError()
