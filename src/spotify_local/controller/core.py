from collections import defaultdict, OrderedDict
from uuid import uuid4


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
        self._registered_events[event][str(uuid)] = func

    def emit(self, event, *args, **kwargs):
        for func in self._registered_events[event].values():
            func(*args, **kwargs)
