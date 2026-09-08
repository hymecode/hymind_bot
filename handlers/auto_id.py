from aiogram import Router, F
from aiogram.types import Message
from config import ADMIN_IDS, GROUP_ID   # GROUP_ID ni ham import qilamiz

router = Router(name="auto_id")

@router.message()
async def auto_send_id(message: Message):
    # Faqat adminlar uchun
    if message.from_user.id not in ADMIN_IDS:
        return

    # Botning o'z xabarlariga javob bermaymiz
    if message.from_user.id == message.bot.id:
        return

    # Matn "/" bilan boshlansa (buyruq bo'lsa), e'tiborsiz qoldiramiz
    if message.text and message.text.startswith("/"):
        return

    # ⬇️ MANA SHU YERGA YOZASIZ ⬇️
    # Faqat bitta guruh uchun ishlatish (agar boshqa guruhda ishlamasin desangiz):
    if message.chat.id != GROUP_ID:
        return
    # ⬆️ MANA SHU YERGA YOZASIZ ⬆️

    await message.reply(
        f"✅ Chat ID: `{message.chat.id}`\n"
        f"✅ Message ID: `{message.message_id}`",
        parse_mode="Markdown"
    )