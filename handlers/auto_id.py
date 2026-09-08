from aiogram import Router
from aiogram.types import Message

router = Router(name="auto_id")

@router.message()
async def catch_all(message: Message):
    print(f"DEBUG: Men xabar oldim! Chat: {message.chat.id} User: {message.from_user.id} Thread: {message.message_thread_id}")
    # Hozircha barchaga javob beramiz (admin tekshiruvi yo'q)
    await message.reply(
        f"✅ Xabar keldi!\n"
        f"Chat ID: `{message.chat.id}`\n"
        f"Message ID: `{message.message_id}`\n"
        f"Topic ID: `{message.message_thread_id}`"
    )