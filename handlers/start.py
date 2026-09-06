from aiogram import Router, types
from aiogram.filters import Command
from keyboards.main import get_main_keyboard

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🧠 **HyMind** botiga xush kelibsiz!\n\n"
        "Quyidagi bo'limlardan birini tanlang:",
        reply_markup=get_main_keyboard(),
        parse_mode="Markdown"
    )