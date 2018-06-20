import sys
import asyncio

import aiohttp
import keyboard

from random import choices
from string import ascii_lowercase
from multiprocessing import Process, queues, get_context
from typing import Dict, Union, Mapping, Callable, Optional

from requests import session, Response, Session

from .event import Event
from .update_status import UpdateStatus

from ..utils import get_url
from ..config import DEFAULT_ORIGIN


class SpotifyLocal:
    """A basic controller for the local Spotify client."""

    __slots__ = [
        "_session",
        "_origin",
        "_connected",
        "_oauth_token",
        "_csrf_token",
        "_process",
        "on_status_change",
    ]

    def __init__(self) -> None:
        self._session: Session = session()
        self._origin: Dict = DEFAULT_ORIGIN
        self._connected: bool = False
        self._oauth_token: str
        self._csrf_token: str
        self._process: Optional[UpdateStatus] = None
        self.on_status_change: Event = Event()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *args):
        self._session.close()
        self.disconnect()

    def _request(self, url: str, params: Dict = {}) -> Response:
        """Makes a request using the currently open session.
        :param url: A url fragment to use in the creation of the master url
        """
        r: Response = self._session.get(url=url, params=params, headers=self._origin)
        return r

    def _get_oauth_token(self) -> str:
        """Retrieve a simple OAuth Token for use with the local http client."""
        url: str = "{0}/token".format(self._origin["Origin"])
        r: Response = self._session.get(url=url)
        return r.json()["t"]

    def _get_csrf_token(self) -> str:
        """Retrieve a simple csrf token for to prevent cross site request forgery."""
        url: str = get_url("/simplecsrf/token.json")
        r = self._request(url=url)
        return r.json()["token"]

    def _check_if_connected(self) -> None:
        """Checks to see if we have connected to the spotify client, essentially a "isSpotifyOpen" check"""
        try:
            assert self._connected == True
        except AssertionError:
            raise ConnectionError(
                "Please either use with context, or call SpotifyLocal.connect() before calling this method."
            )

    def connect(self) -> None:
        """Register the oauth token, the csrf token, and set connected to true"""
        self._oauth_token = self._get_oauth_token()
        self._csrf_token = self._get_csrf_token()
        self._connected = True

    def disconnect(self) -> None:
        """Join the process and set the connection to false."""
        if self._process is not None:
            self._process.should_run = False
            self._process.join()
        self._connected = False

    @property
    def version(self):
        """Spotify version information"""
        url: str = get_url("/service/version.json")
        params = {"service": "remote"}
        r = self._request(url=url, params=params)
        return r.json()

    def get_current_status(self) -> Mapping:
        """Returns the current state of the local spotify client"""
        self._check_if_connected()
        url: str = get_url("/remote/status.json")
        params = {"oauth": self._oauth_token, "csrf": self._csrf_token}
        r = self._request(url=url, params=params)
        return r.json()

    def pause(self, pause=True) -> None:
        """Pauses the spotify player
        :param pause: boolean value to choose the pause/play state
        """
        self._check_if_connected()
        url: str = get_url("/remote/pause.json")
        params = {
            "oauth": self._oauth_token,
            "csrf": self._csrf_token,
            "pause": "true" if pause else "false",
        }
        self._request(url=url, params=params)

    def unpause(self) -> None:
        """Unpauses the player by calling pause()"""
        self.pause(pause=False)

    def playURI(self, uri: str) -> Mapping:
        """Play a Spotify uri, for example spotify:track:5Yn8WCB4Dqm8snemB5Mu4K"""
        self._check_if_connected()
        url: str = get_url("/remote/play.json")
        params = {
            "oauth": self._oauth_token,
            "csrf": self._csrf_token,
            "uri": uri,
            "context": uri,
        }
        r = self._request(url=url, params=params)
        return r.json()

    @staticmethod
    def skip() -> None:
        """Skips the current song"""
        if sys.platform == "darwin":
            keyboard.send("KEYTYPE_SKIP")
        else:
            keyboard.send("next track")

    @staticmethod
    def previous() -> None:
        """Goes to the beginning of the track, or if called twice goes to the previous track."""
        if sys.platform == "darwin":
            keyboard.send("KEYTYPE_PREVIOUS")
        else:
            keyboard.send("previous track")

    def listen_for_events(self, wait: int = 60) -> None:
        """Listen for events and call any associated callbacks when there is an event.
        This is a non-blocking operation.
        """
        self._check_if_connected()
        url: str = get_url("/remote/status.json")
        params: Dict = {"oauth": self._oauth_token, "csrf": self._csrf_token}
        self._process = UpdateStatus(
            handlers=self.on_status_change,
            params=params,
            headers=self._origin,
            url=url,
            wait=wait,
        )
        self._process.start()

