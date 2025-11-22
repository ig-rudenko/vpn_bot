import os
from uuid import UUID


class XRAYConnectionMaker:
    def __init__(self):
        self._server_ip = os.getenv("XRAY_SERVER_IP")
        self._public_key = os.getenv("XRAY_PUBLIC_KEY")
        self._type = "tcp"
        self._port = int(os.getenv("XRAY_PORT", 443))
        self._sni = os.getenv("XRAY_SNI", "yahoo.com")
        self._sid = os.getenv("XRAY_SHORT_ID")  # short id
        self._flow = os.getenv("XRAY_FLOW", "xtls-rprx-vision")  # flow
        self._fp = os.getenv("XRAY_FP", "random")  # FingerPrint
        self._security = os.getenv("XRAY_SECURITY", "reality")

    def get_connection_string(self, uuid: UUID, username: str) -> str:
        return (
            f"vless://{uuid}@{self._server_ip}:{self._port}"
            f"?type={self._type}&"
            f"security={self._security}&"
            f"pbk={self._public_key}&"
            f"fp={self._fp}"
            f"&flow={self._flow}&"
            f"encryption=none"
            f"&sni={self._sni}&"
            f"sid={self._sid}#VLESS-{username}"
        )


xray_connection_maker = XRAYConnectionMaker()
