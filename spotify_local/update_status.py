import requests

from multiprocessing import Process, queues
from typing import Callable, Mapping, Union

from .event import Event


class UpdateStatus(Process):
    def __init__(
        self, handlers: Event, params: Mapping, headers: Mapping, url: str
    ) -> None:
        self.params = params
        self.headers = headers
        self.url = url
        self.session = requests.Session()
        self.handlers = handlers
        super(UpdateStatus, self).__init__()

    def run(self):
        while True:
            self.params["returnon"] = "login,logout,play,pause,error,ap"
            self.params["returnafter"] = 60
            r: Response = self.session.get(
                url=self.url, params=self.params, headers=self.headers
            )
            j = r.json()
            self.handlers(j)
