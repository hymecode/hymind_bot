from aiogram import Router, types
from aiogram.filters import Command
from keyboards.main import get_main_keyboard

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    from utils.database import create_user, get_user
    
    # Foydalanuvchini bazaga qo'shish
    user = get_user(message.from_user.id)
    if not user:
        create_user(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name
        )
    
    await message.answer(
        "🧠 **HyMind** botiga xush kelibsiz!\n\n"
        "Men sizning ongingizni rivojlantirishga yordam beraman.\n"
        "Quyidagi bo'limlardan birini tanlang:",
        reply_markup=get_main_keyboard(),
        parse_mode="Markdown"
    )