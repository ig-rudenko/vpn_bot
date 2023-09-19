import io
import re

import aiohttp
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import VerticalGradiantColorMask
from PIL.Image import Image


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


def generate_qr_code(data: str) -> bytes:
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data(data)
    image: Image = qr.make_image(
        image_factory=StyledPilImage, color_mask=VerticalGradiantColorMask()
    ).get_image()
    image_data = io.BytesIO()
    image.save(image_data, format="PNG")
    return image_data.getvalue()
