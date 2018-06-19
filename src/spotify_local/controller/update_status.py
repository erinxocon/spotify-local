import sys

import requests

from multiprocessing import Process, queues
from typing import Callable, Mapping, Union, Dict

from .event import Event


class UpdateStatus(Process):
    """A process that listens for events from the spotify client and call registered functions"""

    def __init__(
        self, handlers: Event, params: Dict, headers: Dict, url: str, wait: int
    ) -> None:
        self.params: Dict = params
        self.headers: Dict = headers
        self.url: str = url
        self.session: requests.Session = requests.Session()
        self.handlers: Event = handlers
        self.wait: int = wait
        self._should_run = True
        super(UpdateStatus, self).__init__()

    @property
    def should_run(self) -> bool:
        """Should the process continue to listen to events"""
        return self._should_run

    @should_run.setter
    def should_run(self, val: bool) -> None:
        """Set whether or not the process should continue to listen"""
        self._should_run = val

    def run(self) -> None:
        """This is the main process that listens for events using the returnon and returnafter parameters"""
        while self.should_run:
            self.params["returnon"] = "login,logout,play,pause,error,ap"
            self.params["returnafter"] = str(self.wait)
            r: requests.Response = self.session.get(
                url=self.url, params=self.params, headers=self.headers
            )
            j = r.json()
            self.handlers(j)
