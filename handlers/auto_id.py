from aiogram import Router, F
from aiogram.types import Message
from config import ADMIN_IDS, GROUP_ID

router = Router(name="auto_id")

@router.message()
async def auto_send_id(message: Message):
    # 1. Faqat o'sha maxsus yopiq guruhda ishlaydi
    if message.chat.id != GROUP_ID:
        return

    # 2. Kim yuborayotganini tekshiramiz (guruh profili yoki shaxsiy admin)
    is_personal_admin = message.from_user.id in ADMIN_IDS
    is_group_profile = message.sender_chat is not None and message.sender_chat.id == GROUP_ID

    # Agar ikkalasi ham bo'lmasa, e'tiborsiz qoldiramiz
    if not is_personal_admin and not is_group_profile:
        return

    # 3. Botning o'z xabarlariga javob bermaymiz (cheksiz aylanishni oldini olish)
    if message.from_user.id == message.bot.id:
        return
    if message.sender_chat and message.sender_chat.id == message.bot.id:
        return

    # 4. Buyruqlarga ("/" bilan boshlangani) javob bermaymiz
    if message.text and message.text.startswith("/"):
        return

    # 5. ID larni qaytaramiz
    await message.reply(
        f"✅ Chat ID: `{message.chat.id}`\n"
        f"✅ Message ID: `{message.message_id}`\n"
        f"✅ Sender: `{message.from_user.id}`",
        parse_mode="Markdown"
    )