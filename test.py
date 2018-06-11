from pprint import pprint
from spotify_local import SpotifyLocal


if __name__ == "__main__":
    with SpotifyLocal() as s:
        pprint(s.get_current_status())
