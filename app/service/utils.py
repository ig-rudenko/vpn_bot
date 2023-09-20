import io
import random
import re

import aiohttp
import qrcode
from aiohttp import ClientTimeout
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import VerticalGradiantColorMask
from PIL.Image import Image


class CheckURLAvailability:
    def __init__(self, url: str):
        self._url = url
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
        ]

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
            url = "https://" + url
        return url

    async def get_status_code(self) -> int:
        print(self._validate_url(self._url))
        async with aiohttp.ClientSession(
            timeout=ClientTimeout(2.5),
            headers={"user-agent": random.choice(self.user_agents)},
        ) as client:
            async with client as session:
                resp = await session.get(self._validate_url(self._url))
                print(await resp.text())
                resp.close()
                return resp.status


def generate_qr_code(data: str) -> bytes:
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data(data)
    image: Image = qr.make_image(
        image_factory=StyledPilImage, color_mask=VerticalGradiantColorMask()
    ).get_image()
    image_data = io.BytesIO()
    image.save(image_data, format="PNG")
    return image_data.getvalue()
