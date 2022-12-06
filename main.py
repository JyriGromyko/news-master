import asyncio

from config import BACKGROUND_RELOAD
from countries import sync_countries
from news import sync_macronews, sync_world_news
from webserver import WebServer


async def main():
    await asyncio.gather(*([
        server.run()] + ([sync_macronews(), sync_world_news(), sync_countries()
    ] if BACKGROUND_RELOAD else [])))




server = WebServer()
asyncio.run(main(), debug=False)
