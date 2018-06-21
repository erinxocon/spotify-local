import sys

try:
    assert sys.version_info.major == 3
    assert sys.version_info.minor > 2
except AssertionError:
    raise RuntimeError("Spotify-Local requires Python 3.6+!")

from .core import SpotifyLocal
from .utils import (
    is_spotify_running,
    is_spotify_web_helper_running,
    start_spotify_web_helper,
    start_spotify,
)

__version__ = "0.3.1"

