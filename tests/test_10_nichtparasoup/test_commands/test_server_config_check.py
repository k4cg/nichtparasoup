import unittest

from ddt import data, ddt, unpack  # type: ignore

from nichtparasoup.commands.server_config_check import make_probe_status_callback
from nichtparasoup.imagecrawlers.echo import Echo
from nichtparasoup.testing.config import ConfigProbeCallbackReason


@ddt
class MakeProbeStatusCallbackTest(unittest.TestCase):

    __CALLBACK_PARAM_COMBINATIONS = [(False, False), (False, True), (True, False), (True, True)]

    @data(*__CALLBACK_PARAM_COMBINATIONS)  # type: ignore
    @unpack  # type: ignore
    def test_start(self, fail_fast: bool, verbose: bool) -> None:
        # arrange
        callback = make_probe_status_callback(fail_fast=fail_fast, verbose=verbose)
        # act
        callback(ConfigProbeCallbackReason.start, Echo(image_uri='https://foo.bar'), None)
        # assert
        # return does not matter

    @data(*__CALLBACK_PARAM_COMBINATIONS)  # type: ignore
    @unpack  # type: ignore
    def test_finish(self, fail_fast: bool, verbose: bool) -> None:
        # arrange
        callback = make_probe_status_callback(fail_fast=fail_fast, verbose=verbose)
        # act
        callback(ConfigProbeCallbackReason.finish, Echo(image_uri='https://foo.bar'), None)
        # assert
        # return does not matter

    @data(*__CALLBACK_PARAM_COMBINATIONS)  # type: ignore
    @unpack  # type: ignore
    def test_retry(self, fail_fast: bool, verbose: bool) -> None:
        callback = make_probe_status_callback(fail_fast=fail_fast, verbose=verbose)
        res = callback(ConfigProbeCallbackReason.retry, Echo(image_uri='https://foo.bar'), Exception())
        self.assertIs(True, res)

    @data(*__CALLBACK_PARAM_COMBINATIONS)  # type: ignore
    @unpack  # type: ignore
    def test_failure(self, fail_fast: bool, verbose: bool) -> None:
        callback = make_probe_status_callback(fail_fast=fail_fast, verbose=verbose)
        res = callback(ConfigProbeCallbackReason.failure, Echo(image_uri='https://foo.bar'), Exception())
        self.assertIs(not fail_fast, res)
