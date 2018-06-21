import sys

try:
    assert sys.version_info.major == 3
    assert sys.version_info.minor > 2
except AssertionError:
    raise RuntimeError("Spotify-Local requires Python 3.6+!")

from .core import SpotifyLocal

__version__ = "0.3.1"

