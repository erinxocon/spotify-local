from spotify_local import SpotifyLocal, is_spotify_web_helper_running
from time import sleep

print(is_spotify_web_helper_running())
s = SpotifyLocal()


@s.on_play_state_change
def test(status):
    print("Play Pause Engaged")


@s.on_status_change
def test1(status):
    print("new status")


@s.on_track_change
def test2(status):
    print("track changed")


print(s._registered_events)

s.listen(blocking=True)

print("let's see if this prints out")

sleep(120)

