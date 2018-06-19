import asyncio

from spotify_local import SpotifyLocalAsync


ioloop = asyncio.get_event_loop()


async def test():
    async with SpotifyLocalAsync(loop=ioloop, workers=5) as s:
        print(await s.version)


async def test2():
    async with SpotifyLocalAsync(loop=ioloop, workers=5) as s:
        print(await s.get_current_status())


ioloop.run_until_complete(test())
ioloop.run_until_complete(test2())
ioloop.close()
