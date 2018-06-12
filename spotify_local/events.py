import requests

from multiprocessing import Process, queues
from typing import Callable, Mapping, Union


class UpdateStatus(Process):
    def __init__(
        self, callback: Callable, params: Mapping, headers: Mapping, url: str
    ) -> None:
        self.callback = callback
        self.params = params
        self.headers = headers
        self.url = url
        self.session = requests.Session()
        super(UpdateStatus, self).__init__()

    def run(self):
        while True:
            self.params["returnon"] = "login,logout,play,pause,error,ap"
            self.params["returnafter"] = 60
            r: Response = self.session.get(
                url=self.url, params=self.params, headers=self.headers
            )
            j = r.json()
            self.callback(j)

