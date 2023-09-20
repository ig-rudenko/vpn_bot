from datetime import datetime
from typing import Sequence
from uuid import uuid4

from ..models import VPNConnection
from ..xray.service import xray_service
from ..xray.generator import xray_connection_maker
from ..xray.config import config_reader_writer, JSONConfigFormatter


class VPNConnectionService:
    @staticmethod
    async def create_new_connection(
        tg_id: int, username: str, available_to: datetime
    ) -> str:
        user_uuid = uuid4()
        await config_reader_writer.read()

        config = JSONConfigFormatter.to_python(config_reader_writer.config_data)
        config.add_user(protocol="vless", uuid=user_uuid, email=username)

        config_data: str = JSONConfigFormatter.to_write(config)
        await config_reader_writer.write(config_data)

        new_connection_string = xray_connection_maker.get_connection_string(
            uuid=user_uuid, username=username
        )

        await VPNConnection.create(
            uuid=str(user_uuid),
            tg_id=tg_id,
            available_to=available_to,
            username=username,
        )
        await xray_service.reload()
        return new_connection_string

    @staticmethod
    async def get_connections(tg_id: int) -> Sequence[VPNConnection]:
        return await VPNConnection.filter(tg_id=tg_id)
