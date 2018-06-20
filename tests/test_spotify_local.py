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

s = SpotifyLocal()


@s.on("test")
def test(status):
    print(status)


@s.on("test")
def test1(status):
    print(status)


print(s.listeners("test"))

