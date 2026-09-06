from aiogram import Router, types, F
from utils.database import get_db
import logging

router = Router()

# O'ZINGIZNING GURUH ID'NGIZ
CHAT_ID = -1003863295329

# VAQTINCHA: BARCHA GURUHLARDAGI MUSIQALARNI ESHITISH (sinov uchun)
@router.message(F.audio | F.voice | F.document)
async def test_all_music(message: types.Message):
    if message.chat.id == CHAT_ID:
        await message.reply(f"🔍 Musiqa topildi! Chat ID: {message.chat.id}, Message ID: {message.message_id}")
        # Saqlash funksiyasini chaqiramiz
        await save_song(message)

async def save_song(message: types.Message):
    try:
        conn = get_db()
        
        if message.audio:
            file_id = message.audio.file_id
            file_type = "audio"
        elif message.voice:
            file_id = message.voice.file_id
            file_type = "voice"
        elif message.document:
            file_id = message.document.file_id
            file_type = "document"
        else:
            await message.reply("❌ Bu fayl turi qo'llab-quvvatlanmaydi.")
            return
        
        caption = message.caption or ""
        
        conn.execute(
            "INSERT INTO songs (chat_id, message_id, file_id, caption, file_type) VALUES (?, ?, ?, ?, ?)",
            (message.chat.id, message.message_id, file_id, caption, file_type)
        )
        conn.commit()
        conn.close()
        
        await message.reply(f"✅ Musiqa bazaga saqlandi! (ID: {message.message_id})")
        
    except Exception as e:
        await message.reply(f"❌ Xatolik: {e}")
        logging.error(f"Musiqa saqlash xatosi: {e}")

# So'zlar uchun (faqat guruhdan)
@router.message(F.chat.id == CHAT_ID, F.text)
async def save_word(message: types.Message):
    if message.from_user.is_bot:
        return
    try:
        conn = get_db()
        if message.text and not message.caption:
            conn.execute("INSERT INTO words (content) VALUES (?)", (message.text,))
            conn.commit()
            conn.close()
            await message.reply("✅ So'z bazaga saqlandi!")
    except Exception as e:
        await message.reply(f"❌ Xatolik (so'z): {e}")
        logging.error(f"So'z saqlash xatosi: {e}")