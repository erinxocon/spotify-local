import sys

import requests

from multiprocessing import Process, queues
from typing import Callable, Mapping, Union, Dict

from .event import Event


class UpdateStatus(Process):
    def __init__(
        self, handlers: Event, params: Dict, headers: Dict, url: str, wait: int
    ) -> None:
        self.params: Dict = params
        self.headers: Dict = headers
        self.url: str = url
        self.session: requests.Session = requests.Session()
        self.handlers: Event = handlers
        self.wait: int = wait
        super(UpdateStatus, self).__init__()

    def run(self) -> None:
        while True:
            self.params["returnon"] = "login,logout,play,pause,error,ap"
            self.params["returnafter"] = str(self.wait)
            r: requests.Response = self.session.get(
                url=self.url, params=self.params, headers=self.headers
            )
            j = r.json()
            self.handlers(j)
