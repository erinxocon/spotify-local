import sys

from threading import Thread
from collections import defaultdict, OrderedDict

from requests import Session

from .config import DEFAULT_ORIGIN
from .utils import get_url, get_csrf_token, get_oauth_token


class SpotifyLocal:
    """Controller for the local spotify web helper, throws events when the
    state of spotify changes.
    """

    def __init__(self):
        self._registered_events = defaultdict(OrderedDict)
        self._csrf_token = get_csrf_token()
        self._oauth_token = get_oauth_token()
        self._session = Session()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def _request(self, url, params={}):
        """Makes a request using the currently open session.
        :param url: A url fragment to use in the creation of the master url
        """
        r = self._session.get(url=url, params=params, headers=DEFAULT_ORIGIN)
        return r

    def close(self):
        self._session.close()

    def on(self, event):
        """Decorator function that adds function to callback list for event system
        There are three events you can subscribe too:
            - status_change
            - play_state_change
            - track_change
        :param event: name of the event you wish to register the function under, you can use multiple decorators
        """

        def _on(func):
            self.add_event_handler(event, func)
            return func

        return _on

    def add_event_handler(self, event, func):
        """Add function and event to Ordered Dict
        :param event: Name of the event you wish to register the function
        :param func: Function to register witht the associated event
        """
        self._registered_events[event][func] = func

    def emit(self, event, *args, **kwargs):
        """Send out an event and call it's associated functions
        :param event: Name of the event to trigger
        """
        for func in self._registered_events[event].values():
            func(*args, **kwargs)

    def remove_listener(self, event, func):
        """Remove an event listner
        :param event: Event you wish to remove the function from
        :param func: Function you wish to remove
        """
        self._registered_events[event].pop(func)

    def remove_all_listeners(self, event=None):
        """Remove all functions for all events, or one event if one is specifed.
        :param event: Optional event you wish to remove all functions from
        """
        if event is not None:
            self._registered_events[event] = OrderedDict()
        else:
            self._registered_events = defaultdict(OrderedDict)

    def listeners(self, event):
        """Return list of listners associated to a particular event
        :param event: Name of the event you wish to query
        """
        return list(self._registered_events[event].keys())

    @property
    def version(self):
        """Spotify version information"""
        url: str = get_url("/service/version.json")
        params = {"service": "remote"}
        r = self._request(url=url, params=params)
        return r.json()

    def get_current_status(self):
        """Returns the current state of the local spotify client"""
        url = get_url("/remote/status.json")
        params = {"oauth": self._oauth_token, "csrf": self._csrf_token}
        r = self._request(url=url, params=params)
        return r.json()

    def pause(self, pause=True):
        """Pauses the spotify player
        :param pause: boolean value to choose the pause/play state
        """
        url: str = get_url("/remote/pause.json")
        params = {
            "oauth": self._oauth_token,
            "csrf": self._csrf_token,
            "pause": "true" if pause else "false",
        }
        self._request(url=url, params=params)

    def unpause(self):
        """Unpauses the player by calling pause()"""
        self.pause(pause=False)

    def playURI(self, uri):
        """Play a Spotify uri, for example spotify:track:5Yn8WCB4Dqm8snemB5Mu4K"""
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
    def skip():
        """Skips the current song"""
        if sys.platform == "darwin":
            keyboard.send("KEYTYPE_SKIP")
        else:
            keyboard.send("next track")

    @staticmethod
    def previous():
        """Goes to the beginning of the track, or if called twice goes to the previous track."""
        if sys.platform == "darwin":
            keyboard.send("KEYTYPE_PREVIOUS")
        else:
            keyboard.send("previous track")

    def listen(self, wait=60, blocking=True) -> None:
        """Listen for events and call any associated callbacks when there is an event.
        There are three events you can subscribe too:
            - status_change
            - play_state_change
            - track_change

        :param wait: how long to wait for a response before starting a new connection
        :param blocking: if listen should block the current process or not
        """
        url = get_url("/remote/status.json")

        def listen_for_status_change():
            params = {"oauth": self._oauth_token, "csrf": self._csrf_token}
            r = self._request(url=url, params=params)
            old = r.json()
            self.emit("status_change", old)
            params = {
                "oauth": self._oauth_token,
                "csrf": self._csrf_token,
                "returnon": "play,pause,error,ap",
                "returnafter": wait,
            }
            while True:
                r = self._request(url=url, params=params)
                new = r.json()

                if new != old:
                    self.emit("status_change", new)

                if new["playing"] != old["playing"]:
                    self.emit("play_state_change", new)

                if (
                    new["track"]["track_resource"]["uri"]
                    != old["track"]["track_resource"]["uri"]
                ):
                    self.emit("track_change", new)

                old = new

        if blocking:
            listen_for_status_change()
        else:
            thread = Thread(target=listen_for_status_change)
            thread.daemon = True
            thread.start()
