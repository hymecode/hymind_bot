"""
handlers/downloads.py
----------------------
Bot qaysi bo'limda/holatda turgan bo'lishidan qat'i nazar, foydalanuvchi
xabarida havola (link) bo'lsa, ushbu handler uni ushlab qoladi.
"""

import logging
import re
import uuid

from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile, InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from downloader import cleanup_file, download_media

logger = logging.getLogger(__name__)
router = Router(name="downloads")

URL_REGEX = re.compile(r"https?://\S+")
PENDING_LINKS: dict[str, str] = {}

def extract_url(text: str | None) -> str | None:
    if not text:
        return None
    match = URL_REGEX.search(text)
    return match.group(0) if match else None

@router.message(F.text.regexp(URL_REGEX))
async def link_received(message: Message) -> None:
    url = extract_url(message.text)
    if not url:
        return

    token = uuid.uuid4().hex[:10]
    PENDING_LINKS[token] = url

    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(text="🎬 Video", callback_data=f"dl:video:{token}"),
        InlineKeyboardButton(text="🎵 Musiqa", callback_data=f"dl:audio:{token}"),
    )
    await message.answer(
        "Havolani qanday yuborishimni xohlaysiz?",
        reply_markup=kb.as_markup(),
    )

@router.callback_query(F.data.startswith("dl:"))
async def handle_download_choice(callback: CallbackQuery) -> None:
    _, mode, token = callback.data.split(":", maxsplit=2)
    url = PENDING_LINKS.pop(token, None)

    if not url:
        await callback.answer(
            "⚠️ Bu havolaning muddati tugagan, qayta yuboring.",
            show_alert=True,
        )
        return

    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)
    status_msg = await callback.message.answer("⏳ Yuklab olinmoqda, biroz kuting...")

    result = None
    try:
        audio_only = mode == "audio"
        result = await download_media(url, audio_only=audio_only)

        if audio_only:
            await callback.message.answer_audio(
                FSInputFile(result.filepath),
                title=result.title,
            )
        else:
            await callback.message.answer_video(
                FSInputFile(result.filepath),
                caption=result.title,
            )
    except Exception as e:
        logger.exception("Havoladan yuklab olishda xatolik: %s", url)
        await callback.message.answer(f"⚠️ Yuklab bo'lmadi: {e}")
    finally:
        if result:
            cleanup_file(result.filepath)
        await status_msg.delete()