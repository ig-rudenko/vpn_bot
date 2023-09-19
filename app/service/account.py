from datetime import datetime

from ..models import User, Profile
from .exc import ProfileAlreadyExist, ProfileDataInvalid


class ProfileService:
    def __init__(self, tg_id: int):
        self.tg_id = tg_id

    @staticmethod
    async def username_is_available(username: str) -> bool:
        try:
            await Profile.get(username=username)
            return False
        except User.DoesNotExists:
            return True

    @staticmethod
    async def exist(tg_id: int) -> bool:
        try:
            user = await User.get(tg_id=tg_id)
            return user.profile is not None
        except User.DoesNotExists:
            return False

    async def create(self, username: str, password: str) -> Profile:
        if not await self.username_is_available(username=username):
            raise ProfileAlreadyExist("Данный username уже занят")
        if await self.exist(tg_id=self.tg_id):
            raise ProfileAlreadyExist("Вы уже зарегистрированы")

        profile = await Profile.create(
            username=username, password=password, date_joined=datetime.now()
        )
        await self.set_profile_to_tg_user(profile, tg_id=self.tg_id)
        return profile

    @staticmethod
    async def set_profile_to_tg_user(profile: Profile, tg_id: int):
        user = await User.get(tg_id=tg_id)
        await user.update(profile=profile.id)

    @staticmethod
    async def get(username: str, password: str) -> Profile:
        try:
            return await Profile.get(username=username, password=password)
        except Profile.DoesNotExists:
            raise ProfileDataInvalid("Неверный пароль!")
