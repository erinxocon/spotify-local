import asyncio

from spotify_local import SpotifyLocalAsync


ioloop = asyncio.get_event_loop()


async def test():
    s = SpotifyLocalAsync(loop=ioloop)
    await s.connect()
    print(await s.version)
    await s.disconnect()


ioloop.run_until_complete(test())
ioloop.close()
