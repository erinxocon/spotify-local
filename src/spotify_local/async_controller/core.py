import sys
import asyncio

import aiohttp
import keyboard

from multiprocessing import Process, queues, get_context
from typing import Dict, Union, Mapping, Callable, Optional

from requests import session, Response, Session

from ..utils import get_url
from ..config import DEFAULT_ORIGIN, DEFAULT_PORT


class SpotifyLocalAsync:
    """A basic async controller for the local spotify client."""

    __slots__ = [
        "_origin",
        "_connected",
        "_oauth_token",
        "_csrf_token",
        "_loop",
        "_session",
    ]

    def __init__(self, loop=None, workers=None) -> None:
        """ Set or create an event loop and a thread pool.
            :param loop: Asyncio lopp to use.
            :param workers: Amount of threads to use for executing async calls.
                If not pass it will default to the number of processors on the
                machine, multiplied by 5.
        """
        self._origin: Dict = DEFAULT_ORIGIN
        self._loop = loop or asyncio.get_event_loop()
        self._session: aiohttp.ClientSession = aiohttp.ClientSession()
        self._oauth_token = ""
        self._csrf_token = ""
        self._connected = False

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.disconnect()

    async def _request(self, url: str, params: Dict = {}):
        async with self._session.get(url, headers=self._origin, params=params) as r:
            return await r.json()

    async def _get_oauth_token(self):
        """Retrieve a simple OAuth Token for use with the local http client."""
        url: str = "{0}/token".format(self._origin["Origin"])
        r = await self._request(url=url)
        return r["t"]

    async def _get_csrf_token(self) -> str:
        """Retrieve a simple csrf token for to prevent cross site request forgery."""
        url: str = get_url("/simplecsrf/token.json")
        r = await self._request(url=url)
        return r["token"]

    async def connect(self) -> None:
        """Register the oauth token, the csrf token, and set connected to true"""
        self._oauth_token = await self._get_oauth_token()
        self._csrf_token = await self._get_csrf_token()
        self._connected = True

    async def disconnect(self) -> None:
        self._connected = False
        await self._session.close()

    def _check_if_connected(self) -> None:
        """Checks to see if we have connected to the spotify client, essentially a "isSpotifyOpen" check"""
        try:
            assert self._connected == True
        except AssertionError:
            raise ConnectionError(
                "Please either use with context, or call SpotifyLocal.connect() before calling this method."
            )

    @property
    async def version(self):
        """Spotify version information"""
        url: str = get_url("/service/version.json")
        params = {"service": "remote"}
        r = await self._request(url=url, params=params)
        return r

    async def get_current_status(self) -> Mapping:
        """Returns the current state of the local spotify client"""
        self._check_if_connected()
        url: str = get_url("/remote/status.json")
        params = {"oauth": self._oauth_token, "csrf": self._csrf_token}
        r = await self._request(url=url, params=params)
        return r

    async def pause(self, pause=True) -> None:
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
        await self._request(url=url, params=params)

    async def unpause(self) -> None:
        """Unpauses the player by calling pause()"""
        await self.pause(pause=False)

    async def playURI(self, uri: str) -> Mapping:
        """Play a Spotify uri, for example spotify:track:5Yn8WCB4Dqm8snemB5Mu4K"""
        self._check_if_connected()
        url: str = get_url("/remote/play.json")
        params = {
            "oauth": self._oauth_token,
            "csrf": self._csrf_token,
            "uri": uri,
            "context": uri,
        }
        r = await self._request(url=url, params=params)
        return r

