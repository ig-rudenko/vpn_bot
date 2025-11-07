import os

import aiohttp
from aiohttp import web

from app.models import VPNConnection
from database.connection import db

app = web.Application()

BOT_TOKEN = os.getenv("TG_TOKEN")
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",")]

db.init("sqlite+aiosqlite:///db.sqlite3")


async def send_tg_message(session: aiohttp.ClientSession, tg_id: int, message: str):
    async with session.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": tg_id, "text": message, "parse_mode": "HTML"},
    ) as response:
        if response.status != 200:
            print("tg_id", tg_id, "message", message, await response.text())


async def send_notification(tg_id: int, message: str):
    async with aiohttp.ClientSession() as session:
        await send_tg_message(session, tg_id, message)
        for admin_id in ADMIN_IDS:
            await send_tg_message(session, admin_id, message)


class WebhookView(web.View):
    async def post(self):
        data: dict = await self.request.json()
        # {"username":"%s","ip":"%s","server":"%s","action":"%s","duration":%d,"timestamp":"%s"}

        try:
            vpn_connection = await VPNConnection.get(username=data["username"])
        except VPNConnection.DoesNotExists:
            return web.Response(text="OK")

        message = f"""
❌ Вы были заблокированы за использование Торрента
🕗 Время блокировки: {data.get('duration', '-')} мин.
🌐 IP: {data.get('ip', '-')}""".strip()

        await send_notification(tg_id=vpn_connection.tg_id, message=message)
        return web.Response(text="OK")


app.add_routes([web.post("/webhook", WebhookView)])

if __name__ == "__main__":
    web.run_app(app, host="127.0.0.1", port=8080)
