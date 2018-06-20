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


with SpotifyLocal() as s:

    @s.on("status_change")
    def test(status):
        print(status)

    @s.on("status_change")
    def test1(status):
        s.pause()

    print(s.listeners("status_change"))

    s.listen_for_events()

