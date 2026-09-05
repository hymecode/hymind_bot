from aiogram import Router, types, F
from utils.database import get_db
from config import ADMIN_IDS  # config.py dan admin ID olamiz

router = Router()

# YOPIQ GURUH ID'SI (o'zingiznikiga almashtiring!)
CHAT_ID = -1003863295329

@router.message(F.chat.id == CHAT_ID, F.audio | F.voice | F.document)
async def save_song(message: types.Message):
    # Adminning o'z xabarlarini filter qilish (ixtiyoriy)
    if message.from_user.id in ADMIN_IDS:
        await message.reply("ℹ️ Admin xabari, saqlanmadi.")
        return
    
    try:
        conn = get_db()
        if message.audio:
            file_id = message.audio.file_id
            file_type = "audio"
        elif message.voice:
            file_id = message.voice.file_id
            file_type = "voice"
        else:
            file_id = message.document.file_id
            file_type = "document"
        
        caption = message.caption or ""
        conn.execute(
            "INSERT INTO songs (file_id, caption, file_type) VALUES (?, ?, ?)",
            (file_id, caption, file_type)
        )
        conn.commit()
        conn.close()
        await message.reply("✅ Musiqa bazaga saqlandi!")
    except Exception as e:
        await message.reply(f"❌ Xatolik: {e}")

@router.message(F.chat.id == CHAT_ID, F.text)
async def save_word(message: types.Message):
    # Adminning o'z xabarlarini saqlamaslik!
    if message.from_user.id in ADMIN_IDS:
        # Admin xabarini "✅ Musiqa..." deb yozsa, words ga saqlanmaydi
        return
    
    try:
        conn = get_db()
        if message.text and not message.caption:
            # Faqat foydalanuvchi xabarlarini saqlash
            conn.execute("INSERT INTO words (content) VALUES (?)", (message.text,))
            conn.commit()
            conn.close()
            await message.reply("✅ So'z bazaga saqlandi!")
    except Exception as e:
        await message.reply(f"❌ Xatolik: {e}")