__all__ = ["ImagecrawlerCommand"]

from logging import DEBUG as L_DEBUG, ERROR as L_ERROR
from typing import Any, Dict, Optional, Type

from nichtparasoup._internals import _LINEBREAK, _log, _logging_init, _message, _message_exception
from nichtparasoup.cli.commands import BaseCommand
from nichtparasoup.core.server import type_module_name_str
from nichtparasoup.imagecrawler import BaseImageCrawler, get_imagecrawlers


class ImagecrawlerCommand(BaseCommand):

    def main(self, options: Dict[str, Any]) -> int:
        active_actions = {k: v for k, v in options.items() if v}  # type: Dict[str, Any]
        if len(active_actions) != 1:
            _message_exception(ValueError('exactly one action required'))
            return 255
        action_name, action_value = active_actions.popitem()
        action = getattr(self, 'run_{}'.format(action_name))
        return action(action_value)  # type: ignore

    def run_list(self, _: Optional[Any] = None) -> int:
        _logging_init(L_DEBUG if self._debug else L_ERROR)
        imagecrawlers = get_imagecrawlers()  # may trigger debug output
        _log('debug', '- List of loaded ImageCrawlers -')
        if len(imagecrawlers) > 0:
            _message(sorted(imagecrawlers.names()))
        else:
            _message_exception(Warning('no ImageCrawler found'))
        return 0

    def run_desc(self, imagecrawler: str) -> int:
        imagecrawler_class = get_imagecrawlers().get_class(imagecrawler)
        if imagecrawler_class:
            self._print_imagecrawler_info(imagecrawler_class)
            return 0
        _message_exception(ValueError('unknown ImageCrawler {!r}'.format(imagecrawler)))
        return 1

    def _print_imagecrawler_info(self, imagecrawler_class: Type[BaseImageCrawler]) -> None:
        bull = ' * '
        imagecrawler_info = imagecrawler_class.info()
        _message(imagecrawler_info.description)
        _message('')
        if imagecrawler_info.long_description:
            _message(imagecrawler_info.long_description)
            _message('')
        if imagecrawler_info.config:
            _message('CONFIG')
            mlen = max(len(k) for k in imagecrawler_info.config.keys())
            _message(_LINEBREAK.join(
                bull + '{key:{mlen}}: {desc}'.format(mlen=mlen, key=key, desc=desc)
                for key, desc
                in imagecrawler_info.config.items()
            ))
            _message('')
        if self._debug:
            _message(_LINEBREAK.join([
                'DEBUG INFO',
                bull + 'Icon : {}'.format(imagecrawler_info.icon_url),
                bull + 'Class: {}'.format(type_module_name_str(imagecrawler_class)),
            ]))
            _message('')
