from typing import Dict


class SpotipyLocal:
    def __init__(self):
        pass

    @property
    def port(self) -> int:
        return 4370

    @property
    def origin(self) -> Dict[str, str]:
        return {"Origin": "https://open.spotify.com"}
