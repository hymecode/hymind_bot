from aiogram import Router, F
from aiogram.types import Message
from config import ADMIN_IDS, GROUP_ID

router = Router(name="auto_id")

@router.message()
async def auto_send_id(message: Message):
    # Terminalga tekshiruv uchun log chiqarish
    print(f"DEBUG: Chat: {message.chat.id}, Sender: {message.from_user.id}, SenderChat: {message.sender_chat}")

    # Faqat o'sha guruhda ishlaydi
    if message.chat.id != GROUP_ID:
        return

    # 1) Shaxsiy akkauntdan yuborilgan xabarni tekshiramiz
    is_personal_admin = message.from_user.id in ADMIN_IDS
    
    # 2) Guruh profili orqali yuborilgan xabarni tekshiramiz
    is_group_profile = message.sender_chat is not None and message.sender_chat.id == GROUP_ID

    # Agar ikkalasi ham bo'lmasa, to'xtaymiz
    if not is_personal_admin and not is_group_profile:
        return

    # Botning o'z xabarlariga javob bermaymiz
    if message.from_user.id == message.bot.id:
        return
    if message.sender_chat and message.sender_chat.id == message.bot.id:
        return

    # Buyruqlarga javob bermaymiz
    if message.text and message.text.startswith("/"):
        return

    # Muhim ID'larni qaytaramiz!
    thread_id = message.message_thread_id if message.message_thread_id else "General (Yo'q)"
    
    await message.reply(
        f"✅ Chat ID: `{message.chat.id}`\n"
        f"✅ Message ID: `{message.message_id}`\n"
        f"✅ Topic ID (thread_id): `{thread_id}`",
        parse_mode="Markdown"
    )