import asyncio

from app.admin_handlers import become, xray_control, server_control, clients_control
from app.handlers import welcome, utils, vpn, profile, install_info, deleter
from app.middleware import LoggingMiddleware
from database.connection import db
from settings import bot, dp


async def main():
    # ==== Routers =====
    dp.include_routers(
        welcome.router,
        install_info.router,
        profile.router,
        utils.router,
        vpn.router,
        become.router,
        xray_control.router,
        server_control.router,
        clients_control.router,
        clients_lead.router,
        deleter.router,
    )

    # ==== Middleware ====
    dp.message.middleware(LoggingMiddleware())
    dp.callback_query.middleware(LoggingMiddleware())

    # ==== Init Database ====
    db.init("sqlite+aiosqlite:///db.sqlite3")
    await db.create_all()

    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
