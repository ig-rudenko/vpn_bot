import aiohttp


class CheckURLAvailability:
    def __init__(self, url: str):
        self._url = url

    async def available(self) -> bool:
        async with aiohttp.ClientSession() as client:
            async with client as session:
                resp = await session.get(self._url)
                return resp.status == 200
