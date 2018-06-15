from pprint import pprint
from spotify_local import SpotifyLocal


def test(new_status):
    pprint(new_status)


if __name__ == "__main__":
    with SpotifyLocal() as s:
        # s.on_status_change += test
        # s.listen_for_events()
        pprint(s.get_current_status())
        print("This should print out")
