import sys

try:
    assert sys.version_info.major == 3
    assert sys.version_info.minor > 5
except AssertionError:
    raise RuntimeError("Spotify-Local requires Python 3.6+!")

from .controller import SpotifyLocal
from .async_controller import SpotifyLocalAsync

__version__ = "0.2.3"

