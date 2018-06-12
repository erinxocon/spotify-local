from pprint import pprint
from spotify_local import SpotifyLocal


def test(new_status):
    print(new_status)


if __name__ == "__main__":
    with SpotifyLocal() as s:
        s.on_track_change(callback=test)
