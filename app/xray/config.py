import json
import pathlib
from typing import Literal
from uuid import UUID

import aiofiles


class Config:
    def __init__(self, config: dict):
        self._config = config

    @property
    def data(self) -> dict:
        return self._config

    def add_user(
        self, protocol: str, uuid: UUID, email: str, flow: str = "xtls-rprx-vision"
    ):
        for inbound in self._config["inbounds"]:
            if inbound["protocol"] == protocol:
                for client in inbound["settings"]["clients"]:
                    if client["id"] == uuid:
                        return
                inbound["settings"]["clients"].append(
                    {
                        "id": str(uuid),
                        "email": email,
                        "flow": flow,
                    }
                )

    def delete_user(self, protocol: str, uuid: UUID):
        uuid_str = str(uuid)
        for inbound in self._config["inbounds"]:
            if inbound["protocol"] == protocol:
                client_index = -1
                for i, client in enumerate(inbound["settings"]["clients"]):
                    if client["id"] == uuid_str:
                        client_index = 1
                        break
                if client_index != -1:
                    inbound["settings"]["clients"].pop(client_index)


class ConfigReaderWriter:
    def __init__(self, path: pathlib.Path):
        self._path = path
        self._config: str | bytes | None = None

    @property
    def config_data(self) -> str:
        if self._config is None:
            return ""
        if isinstance(self._config, bytes):
            return self._config.decode()

    async def read(self, mode: Literal["r", "rb"] = "r") -> None:
        async with aiofiles.open(self._path, mode) as file:
            self._config = await file.read()

    async def write(self, data: str | bytes) -> None:
        if isinstance(data, bytes):
            mode: Literal["wb"] = "wb"
        else:
            mode: Literal["w"] = "w"
        async with aiofiles.open(self._path, mode) as file:
            await file.write(data)


class JSONConfigFormatter:
    @staticmethod
    def to_python(data: str) -> Config:
        return Config(json.loads(data))

    @staticmethod
    def to_write(config: Config) -> str:
        return json.dumps(config.data, indent=4)
