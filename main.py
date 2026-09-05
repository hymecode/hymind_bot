import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from utils.database import init_db
from handlers import setup_handlers

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

init_db()
setup_handlers(dp)

async def main():
    await dp.start_polling(bot, allowed_updates=["message", "callback_query"])

if __name__ == "__main__":
    print("🚀 HyMind bot ishga tushmoqda...")
    asyncio.run(main())