import time

import keyboard

from random import choices
from string import ascii_lowercase
from typing import Dict, Union, List, Any, Optional, Mapping

from requests import session, Response, Session

from pprint import pprint

# define types
_KEYVALUE = Mapping[str, Union[object, str]]


class SpotipyLocal:
    def __init__(self) -> None:
        self.session: Session = session()
        self._origin: _KEYVALUE = {"Origin": "https://open.spotify.com"}
        self._port: int = 4381
        self._status: Mapping = None
        self._oauth_token: str
        self._csrf_token: str

    @property
    def port(self) -> int:
        """Default port that spotify web helper services binds too"""
        return self._port

    @property
    def origin(self) -> _KEYVALUE:
        """Returns the Origin Header for the spotiy api"""
        return self._origin

    def _get_url(self, url: str) -> str:
        sub = "{0}.spotilocal.com".format("".join(choices(ascii_lowercase, k=10)))
        return "http://{0}:{1}{2}".format(sub, self.port, url)

    def _make_request(self, url: str, params: Dict = {}) -> Response:
        r: Response = self.session.get(url=url, params=params, headers=self.origin)
        return r

    @property
    def version(self) -> Mapping[str, Union[int, str]]:
        url: str = self._get_url("/service/version.json")
        params = {"service": "remote"}
        r = self._make_request(url=url, params=params)
        return r.json()

    def _get_oauth_token(self) -> str:
        url: str = "{0}/token".format(self.origin["Origin"])
        r: Response = self.session.get(url=url)
        return r.json()["t"]

    def _get_csrf_token(self) -> str:
        url: str = self._get_url("/simplecsrf/token.json")
        r = self._make_request(url=url)
        return r.json()["token"]

    def connect(self) -> None:
        self._oauth_token = self._get_oauth_token()
        self._csrf_token = self._get_csrf_token()

    def get_status(self) -> Mapping:
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

    def skip(self):
        keyboard.send("next track")

    def previous(self):
        keyboard.send("previous track")


if __name__ == "__main__":
    s = SpotipyLocal()
    s.connect()
    pprint(s.get_status())
