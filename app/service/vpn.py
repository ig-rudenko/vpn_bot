import os
import pathlib
from datetime import datetime
from uuid import uuid4

from ..models import VPNConnection, Profile
from ..xray.service import xray_service
from ..xray.generator import xray_connection_maker
from ..xray.config import ConfigReaderWriter, JSONConfigFormatter


class VPNConnectionService:
    @staticmethod
    async def create_new_connection(
        profile: Profile, username: str, available_to: datetime
    ) -> str:
        user_uuid = uuid4()
        # config_reader_writer = ConfigReaderWriter(
        #     path=pathlib.Path(os.getenv("XRAY_CONFIG_PATH"))
        # )
        # await config_reader_writer.read()
        # config_data = config_reader_writer.config_data
        #
        # config = JSONConfigFormatter.to_python(config_data)
        # config.add_user(protocol="vless", uuid=user_uuid, email=username)
        # config_data = JSONConfigFormatter.to_write(config)
        #
        # await config_reader_writer.write(config_data)

        new_connection_string = xray_connection_maker.get_connection_string(
            uuid=user_uuid, username=username
        )

        await VPNConnection.create(
            uuid=str(user_uuid), profile=profile, available_to=available_to
        )
        # await xray_service.reload()
        return new_connection_string

    @staticmethod
    async def get_connections(profile: Profile) -> list[VPNConnection]:
        connection = await VPNConnection.filter(profile=profile.id)
        return connection
