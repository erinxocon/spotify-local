# import asyncio

# from spotify_local import SpotifyLocalAsync


# ioloop = asyncio.get_event_loop()


# async def test():
#     s = SpotifyLocalAsync(loop=ioloop)
#     await s.connect()
#     print(await s.version)
#     await s.disconnect()


# ioloop.run_until_complete(test())
# ioloop.close()

from spotify_local import SpotifyLocal
from time import sleep

s = SpotifyLocal()


@s.on("play_state_change")
def test(status):
    print("Play Pause Engaged")


# @s.on("status_change")
# def test1(status):
#     print("new status")


@s.on("track_change")
def test2(status):
    print("track changed")


print(s._registered_events)

s.listen_for_events(blocking=True)

print("let's see if this prints out")

sleep(120)
