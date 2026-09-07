# main.py

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from handlers import setup_handlers

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

setup_handlers(dp)

async def main():
    print("🚀 HyMind bot ishga tushmoqda...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())