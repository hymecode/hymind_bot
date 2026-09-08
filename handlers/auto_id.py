from aiogram import Router, F
from aiogram.types import Message
from config import ADMIN_IDS, GROUP_ID

router = Router(name="auto_id")

@router.message()
async def auto_send_id(message: Message):
    # Faqat o'sha guruhda ishlaydi
    if message.chat.id != GROUP_ID:
        return

    # Admin yoki guruh profili tekshiruvi (ikkalasini ham qabul qilamiz)
    is_personal_admin = message.from_user.id in ADMIN_IDS
    is_group_profile = message.sender_chat is not None and message.sender_chat.id == GROUP_ID
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

    # <code> teglari bilan yozamiz - bosib nusxa olish oson bo'ladi
    thread_id = message.message_thread_id if message.message_thread_id else "General"
    
    await message.reply(
        f"✅ Xabar qabul qilindi!\n\n"
        f"Chat ID: <code>{message.chat.id}</code>\n"
        f"Message ID: <code>{message.message_id}</code>\n"
        f"Topic ID: <code>{thread_id}</code>",
        parse_mode="HTML"  # HTML rejimida ishlaydi
    )