import os
from uuid import UUID


class XRAYConnectionMaker:
    def __init__(self):
        self._server_ip = os.getenv("XRAY_SERVER_IP")
        self._public_key = os.getenv("XRAY_PUBLIC_KEY")
        self._type = "tcp"
        self._port = 443
        self._sni = "www.microsoft.com"
        self._sid = os.getenv("XRAY_SHORT_ID")  # short id
        self._flow = "xtls-rprx-vision"

    def get_connection_string(self, uuid: UUID, username: str) -> str:
        return (
            f"vless://{uuid}@{self._server_ip}:{self._port}"
            f"?type={self._type}&security=reality&pbk={self._public_key}&fp=chrome"
            f"&flow={self._flow}&encryption=none"
            f"&sni={self._sni}&sid={self._sid}#VLESS-{username}"
        )


xray_connection_maker = XRAYConnectionMaker()
