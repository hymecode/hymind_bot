import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from handlers import translate, tests, media, support, start, auto_id, downloader

async def main() -> None:
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(translate.router)
    dp.include_router(tests.router)
    dp.include_router(media.router)
    dp.include_router(support.router)
    dp.include_router(start.router)
    dp.include_router(downloader.router)  # 🚀 QO'SHILDI!

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())