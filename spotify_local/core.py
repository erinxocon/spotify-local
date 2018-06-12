import keyboard

from random import choices
from string import ascii_lowercase
from typing import Dict, Union, Mapping, Callable, Optional
from multiprocessing import Process, queues, get_context

from requests import session, Response, Session

from .events import UpdateStatus

# define types
_KEYVALUE = Mapping[str, Union[object, str]]


class SpotifyLocal:
    def __init__(self) -> None:
        self.session: Session = session()
        self._origin: _KEYVALUE = {"Origin": "https://open.spotify.com"}
        self._port: int = 4381
        self._oauth_token: str
        self._csrf_token: str
        self._process: Optional[Process] = None

    def __enter__(self):
        self._oauth_token = self._get_oauth_token()
        self._csrf_token = self._get_csrf_token()
        return self

    def __exit__(self, *args):
        if self._process is not None:
            self._process.join()

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

    @property
    def version(self):
        url: str = self._get_url("/service/version.json")
        params = {"service": "remote"}
        r = self._make_request(url=url, params=params)
        return r.json()

    def get_current_status(self) -> Mapping:
        url: str = self._get_url("/remote/status.json")
        params = {"oauth": self._oauth_token, "csrf": self._csrf_token}
        r = self._make_request(url=url, params=params)
        return r.json()

    def pause(self, pause=True) -> None:
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

    def on_track_change(self, callback: Callable) -> None:
        url: str = self._get_url("/remote/status.json")
        params = {"oauth": self._oauth_token, "csrf": self._csrf_token}
        self._process = UpdateStatus(
            callback=callback, params=params, headers=self._origin, url=url
        )
        self._process.start()

