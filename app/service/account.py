from datetime import datetime

from aiogram.types import User as TGUser

from ..models import User
from .exc import ProfileAlreadyExist


class Profile:
    def __init__(self, tg_user: TGUser = None):
        self.tg_user: TGUser | None = tg_user

    @staticmethod
    async def username_is_available(username: str) -> bool:
        try:
            await User.get(profile_username=username)
            return False
        except User.DoesNotExists:
            return True

    @staticmethod
    async def exist(tg_id: int) -> bool:
        try:
            await User.get(tg_id=tg_id)
            return True
        except User.DoesNotExists:
            return False

    async def create(self, username: str, password: str) -> User:
        if not await self.username_is_available(username=username):
            raise ProfileAlreadyExist("Данный username уже занят")
        if await self.exist(tg_id=self.tg_user.id):
            raise ProfileAlreadyExist("Вы уже зарегистрированы")

        return await User.create(
            profile_username=username,
            profile_password=password,
            date_joined=datetime.now(),
            tg_id=self.tg_user.id,
            tg_username=self.tg_user.username,
            first_name=self.tg_user.first_name,
            last_name=self.tg_user.last_name,
        )
