import os
import re
import logging
from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from yt_dlp import YoutubeDL
import imageio_ffmpeg

logger = logging.getLogger(__name__)
router = Router(name="downloader")

URL_PATTERN = re.compile(
    r"((https?://)?(www\.)?(youtube\.com|youtu\.be|instagram\.com|tiktok\.com|facebook\.com|vm\.tiktok\.com|twitter\.com|x\.com)/[^\s]+)"
)

class DownloaderStates(StatesGroup):
    waiting_for_choice = State()

@router.message(F.text.regexp(URL_PATTERN))
async def detect_url(message: Message, state: FSMContext):
    match = URL_PATTERN.search(message.text)
    if not match:
        return
    url = match.group(0)
    await state.set_state(DownloaderStates.waiting_for_choice)
    await state.update_data(url=url)

    kb = InlineKeyboardBuilder()
    kb.button(text="🎬 Video yuklab olish", callback_data="dl:video")
    kb.button(text="🎵 Musiqa (MP3) yuklab olish", callback_data="dl:audio")
    kb.adjust(1)
    await message.answer("Nima yuklab olay? Tanlang:", reply_markup=kb.as_markup())

@router.callback_query(DownloaderStates.waiting_for_choice, F.data.startswith("dl:"))
async def download_media(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer("⏳ Yuklanmoqda...")
    data = await state.get_data()
    url = data.get("url")
    choice = callback_query.data.split(":")[1]
    await state.clear()

    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

    # 🔥 YouTube bot-deteksiyasini chetlab o'tish uchun:
    # - player_client: tv, mweb, web (birinchi ishlaydiganini sinab ko'radi)
    # - http_headers: User-Agent qo'shamiz (brauzer kabi ko'rinish)
    # - cookies: agar "cookies.txt" fayli mavjud bo'lsa, undan foydalanamiz (ixtiyoriy)
    ydl_opts = {
        "outtmpl": "./downloads/%(title)s.%(ext)s",
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "noplaylist": True,
        "quiet": True,
        "ffmpeg_location": ffmpeg_path,
        "extractor_args": {
            "youtube": {
                "player_client": ["tv", "mweb", "web"]
            }
        },
        "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        },
        # Agar loyihada "cookies.txt" bo'lsa, avtomatik qo'llaymiz
        "cookiefile": "cookies.txt" if os.path.exists("cookies.txt") else None,
    }

    if choice == "audio":
        ydl_opts["format"] = "bestaudio/best"
        ydl_opts["postprocessors"] = [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ]

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            if choice == "audio":
                base, _ = os.path.splitext(filename)
                filename = base + ".mp3"

            file_size = os.path.getsize(filename)
            if file_size > 50 * 1024 * 1024:
                await callback_query.message.answer("❌ Fayl juda katta (50MB dan oshadi). Kichikroq sifatda yuklab oling.")
                os.remove(filename)
                return

            with open(filename, "rb") as f:
                if choice == "video":
                    await callback_query.message.answer_video(f, caption="✅ Video muvaffaqiyatli yuklandi!")
                else:
                    await callback_query.message.answer_audio(f, caption="✅ Musiqa muvaffaqiyatli yuklandi!")

            os.remove(filename)

    except Exception as e:
        logger.exception("Yuklab olishda xatolik: %s", e)
        await callback_query.message.answer(
            f"❌ Yuklab olishda xatolik yuz berdi:\n<code>{e}</code>",
            parse_mode="HTML"
        )