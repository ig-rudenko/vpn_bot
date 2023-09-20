from .models import User, Profile


async def get_user(tg_id: int) -> User:
    user = await User.get(tg_id=tg_id)
    profile = await Profile.get(id=user.profile)
    user.profile = profile
    return user
