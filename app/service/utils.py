import re

import aiohttp


class CheckURLAvailability:
    def __init__(self, url: str):
        self._url = url

    @staticmethod
    def _validate_url(url):
        # Проверяем, соответствует ли url регулярному выражению
        match = re.match(r"^(http|https)://\S+", url)
        # Если соответствует, возвращаем url без изменений
        if match:
            return url
        # Если не соответствует, пытаемся исправить url
        # Добавляем префикс http://, если его нет
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        return url

    async def get_status_code(self) -> int:
        async with aiohttp.ClientSession() as client:
            async with client as session:
                resp = await session.get(self._validate_url(self._url))
                resp.close()
                return resp.status
