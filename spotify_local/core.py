import sys

import keyboard

from random import choices
from string import ascii_lowercase
from typing import Dict, Union, Mapping, Callable, Optional
from multiprocessing import Process, queues, get_context

from requests import session, Response, Session

from .event import Event
from .update_status import UpdateStatus

try:
    assert sys.version_info.major == 3
    assert sys.version_info.minor > 5
except AssertionError:
    raise RuntimeError("Spotify-Local-Control requires Python 3.6+!")


DEFAULT_ORIGIN: Dict = {"Origin": "https://open.spotify.com"}
DEFAULT_PORT: int = 4381


class SpotifyLocal:

    __slots__ = [
        "session",
        "_origin",
        "_port",
        "_connected",
        "_oauth_token",
        "_csrf_token",
        "_process",
        "on_status_change",
    ]

    def __init__(self) -> None:
        self.session: Session = session()
        self._origin: Dict = DEFAULT_ORIGIN
        self._port: int = DEFAULT_PORT
        self._connected: bool = False
        self._oauth_token: str
        self._csrf_token: str
        self._process: Optional[Process] = None
        self.on_status_change: Event = Event()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *args):
        self.disconnect()

    def connect(self) -> None:
        self._oauth_token = self._get_oauth_token()
        self._csrf_token = self._get_csrf_token()
        self._connected = True

    def disconnect(self) -> None:
        if self._process is not None:
            self._process.join()
        self._connected = False

    def _get_url(self, url: str) -> str:
        sub = "{0}.spotilocal.com".format("".join(choices(ascii_lowercase, k=10)))
        return "http://{0}:{1}{2}".format(sub, self._port, url)

    def _make_request(self, url: str, params: Dict = {}) -> Response:

        r: Response = self.session.get(url=url, params=params, headers=self._origin)
        return r

    def _get_oauth_token(self) -> str:
        url: str = "{0}/token".format(self._origin["Origin"])
        r: Response = self.session.get(url=url)
        return r.json()["t"]

    def _get_csrf_token(self) -> str:
        url: str = self._get_url("/simplecsrf/token.json")
        r = self._make_request(url=url)
        return r.json()["token"]

    def _check_if_connected(self) -> None:
        try:
            assert self._connected == True
        except AssertionError:
            raise ConnectionError(
                "Please either use with context, or call SpotifyLocal.connect() before calling this method."
            )

    @property
    def version(self):
        url: str = self._get_url("/service/version.json")
        params = {"service": "remote"}
        r = self._make_request(url=url, params=params)
        return r.json()

    def get_current_status(self) -> Mapping:
        self._check_if_connected()
        url: str = self._get_url("/remote/status.json")
        params = {"oauth": self._oauth_token, "csrf": self._csrf_token}
        r = self._make_request(url=url, params=params)
        return r.json()

    def pause(self, pause=True) -> None:
        self._check_if_connected()
        url: str = self._get_url("/remote/pause.json")
        params = {
            "oauth": self._oauth_token,
            "csrf": self._csrf_token,
            "pause": "true" if pause else "false",
        }
        self._make_request(url=url, params=params)

    def unpause(self) -> None:
        self.pause(pause=False)

    def playURI(self, uri: str) -> Mapping:
        self._check_if_connected()
        url: str = self._get_url("/remote/play.json")
        params = {
            "oauth": self._oauth_token,
            "csrf": self._csrf_token,
            "uri": uri,
            "context": uri,
        }
        r = self._make_request(url=url, params=params)
        return r.json()

    def skip(self) -> None:
        keyboard.send("next track")

    def previous(self) -> None:
        keyboard.send("previous track")

    def listen_for_events(self, wait: int = 60) -> None:
        self._check_if_connected()
        url: str = self._get_url("/remote/status.json")
        params: Dict = {"oauth": self._oauth_token, "csrf": self._csrf_token}
        self._process = UpdateStatus(
            handlers=self.on_status_change,
            params=params,
            headers=self._origin,
            url=url,
            wait=wait,
        )
        self._process.start()

