__all__ = ["Server"]

from typing import Optional, Dict, Any

from .nichtparasoup import NichtParasoup


class Server(object):

    def __init__(self, nichtparasoup: NichtParasoup) -> None:
        self.nichtparasoup = nichtparasoup

    def get(self) -> Optional[Dict[str, Any]]:
        image = self.nichtparasoup.get_random_image()
        return None if not image else {
            "uri": image.uri,
            "source": image.source,
            "more": image.more,
        }

    # TODO: write the other server functions
