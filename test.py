from spotify_local import SpotifyLocal


def v():
    with SpotifyLocal() as s:
        print(s.version)


if __name__ == "__main__":
    v()
