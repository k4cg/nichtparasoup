"""All imagecrcrawlers that were shipped with nichtparasoup.
"""

__all__ = [
    'Echo',
    'InstagramHashtag', 'InstagramProfile',
    'Picsum',
    'Pr0gramm',
    'Reddit',
]

from .echo import Echo
from .instagram import InstagramHashtag, InstagramProfile
from .picsum import Picsum
from .pr0gramm import Pr0gramm
from .reddit import Reddit
