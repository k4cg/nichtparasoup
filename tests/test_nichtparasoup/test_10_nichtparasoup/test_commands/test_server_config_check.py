import pytest

from nichtparasoup.commands.server_config_check import make_probe_status_callback
from nichtparasoup.imagecrawlers.echo import Echo
from nichtparasoup.testing.config import ConfigProbeCallbackReason


@pytest.mark.parametrize('verbose', [True, False], ids=['verbose', 'compact'])
@pytest.mark.parametrize('fail_fast', [True, False], ids=['FailFast', 'FailSlow'])
class TestMakeProbeStatusCallback:

    def test_start(self, fail_fast: bool, verbose: bool) -> None:
        # arrange
        callback = make_probe_status_callback(fail_fast=fail_fast, verbose=verbose)
        # act
        callback(ConfigProbeCallbackReason.start, Echo(image_uri='https://foo.bar'), None)
        # assert
        # return does not matter

    def test_finish(self, fail_fast: bool, verbose: bool) -> None:
        # arrange
        callback = make_probe_status_callback(fail_fast=fail_fast, verbose=verbose)
        # act
        callback(ConfigProbeCallbackReason.finish, Echo(image_uri='https://foo.bar'), None)
        # assert
        # return does not matter

    def test_retry(self, fail_fast: bool, verbose: bool) -> None:
        # arrange
        callback = make_probe_status_callback(fail_fast=fail_fast, verbose=verbose)
        # act
        res = callback(ConfigProbeCallbackReason.retry, Echo(image_uri='https://foo.bar'), Exception())
        # assert
        assert isinstance(res, bool)
        assert res is True

    def test_failure(self, fail_fast: bool, verbose: bool) -> None:
        # arrange
        callback = make_probe_status_callback(fail_fast=fail_fast, verbose=verbose)
        # act
        res = callback(ConfigProbeCallbackReason.failure, Echo(image_uri='https://foo.bar'), Exception())
        # assert
        assert isinstance(res, bool)
        assert res is not fail_fast
