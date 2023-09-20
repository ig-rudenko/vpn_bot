import asyncio

from app.handlers import welcome, account, utils, vpn, profile
from database.connection import db
from settings import bot, dp


async def main():
    # ==== Routers =====
    dp.include_routers(
        welcome.router,
        account.router,
        profile.router,
        utils.router,
        vpn.router,
    )

    # ==== Init Database ====
    db.init("sqlite+aiosqlite:///db.sqlite3")
    await db.create_all()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
