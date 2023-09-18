import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage


logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv("TG_TOKEN"))
dp = Dispatcher(storage=MemoryStorage())
