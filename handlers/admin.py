from aiogram import Router, types, F
from utils.database import get_db

router = Router()
CHAT_ID = -1003863295329  # Yopiq guruh ID'ingiz

@router.message(F.chat.id == CHAT_ID, F.audio | F.voice | F.document)
async def save_song(message: types.Message):
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
            "INSERT INTO songs (chat_id, message_id, file_id, caption, file_type) VALUES (?, ?, ?, ?, ?)",
            (message.chat.id, message.message_id, file_id, caption, file_type)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)

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
    except Exception as e:
        print(e)