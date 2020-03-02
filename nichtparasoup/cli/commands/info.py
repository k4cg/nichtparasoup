__all__ = ["InfoCommand"]

from typing import Any, Dict, Optional

from nichtparasoup import VERSION
from nichtparasoup._internals import _log, _message, _message_exception
from nichtparasoup.cli.commands import BaseCommand
from nichtparasoup.core.server import type_module_name_str
from nichtparasoup.imagecrawler import get_imagecrawlers


class InfoCommand(BaseCommand):

    def main(self, options: Dict[str, Any]) -> int:
        active_actions = {k: v for k, v in options.items() if v}  # type: Dict[str, Any]
        if len(active_actions) != 1:
            _message_exception(ValueError('exactly one action required'))
            return 255
        action_name, action_value = active_actions.popitem()
        action = getattr(self, 'run_{}'.format(action_name))
        return action(action_value)  # type: ignore

    @staticmethod
    def run_version(_: Optional[Any] = None) -> int:
        _message(VERSION)
        return 0

    @staticmethod
    def run_imagecrawler_list(_: Optional[Any] = None) -> int:
        imagecrawlers = get_imagecrawlers().names()
        if not imagecrawlers:
            _message_exception(Warning('no ImageCrawler found'))
        else:
            _message("\r\n".join(sorted(imagecrawlers)))
        return 0

    @staticmethod
    def run_imagecrawler_desc(imagecrawler: str) -> int:
        imagecrawler_class = get_imagecrawlers().get_class(imagecrawler)
        if not imagecrawler_class:
            _message_exception(ValueError('unknown ImageCrawler {!r}'.format(imagecrawler)))
            return 1
        info = []
        info_linebreak = '\r\n'
        imagecrawler_info = imagecrawler_class.info()
        info.append(imagecrawler_info.description)
        if imagecrawler_info.long_description:
            info.append(imagecrawler_info.long_description)
        if imagecrawler_info.config:
            info_bull = info_linebreak + ' * '
            mlen = max(len(k) for k in imagecrawler_info.config.keys())
            info.append('Config: ' + info_bull + info_bull.join([
                '{key:{mlen}}: {desc}'.format(mlen=mlen, key=key, desc=desc)
                for key, desc in imagecrawler_info.config.items()]))
        _message((info_linebreak * 2).join(info))
        _log('debug', info_linebreak.join(
            [
                info_linebreak,
                'DEBUG INFO',
                'Icon : {!r}'.format(imagecrawler_info.icon_url),
                'Class: {!r}'.format(type_module_name_str(imagecrawler_class)),
            ]))
        return 0
