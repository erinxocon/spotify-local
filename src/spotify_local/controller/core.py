from collections import defaultdict, OrderedDict
from uuid import uuid4

from ..utils import get_url, get_csrf_token, get_oauth_token
from ..config import DEFAULT_ORIGIN


class SpotifyLocal:
    def __init__(self):
        self._registered_events = defaultdict(OrderedDict)

    def on(self, event):
        def _on(func):
            self.add_event_handler(event, func)
            return func

        return _on

    def add_event_handler(self, event, func):
        uuid = uuid4()
        self._registered_events[event][func] = func

    def emit(self, event, *args, **kwargs):
        for func in self._registered_events[event].values():
            func(*args, **kwargs)

    def remove_listener(self, event, f):
        self._registered_events[event].pop(f)

    def remove_all_listeners(self, event=None):
        if event is not None:
            self._registered_events[event] = OrderedDict()
        else:
            self._registered_events = defaultdict(OrderedDict)

    def listeners(self, event):
        return list(self._registered_events[event].keys())
