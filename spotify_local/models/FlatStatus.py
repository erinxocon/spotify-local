class FlatStatus:
    def __init__(self) -> None:
        self._artist: str
        self._album: str
        self._track: str
        self._track_len: str

    @property
    def artist(self) -> str:
        return self._artist

    @artist.setter
    def artist(self, val) -> None:
        self._artist = val

    @property
    def album(self) -> str:
        return self._album

    @album.setter
    def album(self, val) -> None:
        self._artist = val

    @property
    def track(self) -> str:
        return self._track

    @track.setter
    def track(self, val) -> None:
        self._artist = val

    @property
    def track_len(self) -> str:
        return self._track_len

    @track_len.setter
    def track_len(self, val) -> None:
        self._artist = val
