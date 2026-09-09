"""
downloader.py
--------------
YouTube, Instagram, TikTok va boshqa platformalardan video/audio yuklab
olish uchun yagona modul. Faqat Python kodi bilan ishlaydi.
"""

from __future__ import annotations

import asyncio
import base64
import glob
import logging
import os
import stat
import tempfile
import uuid
from pathlib import Path

import imageio_ffmpeg
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent
BIN_DIR = BASE_DIR / "bin"
RUSTYPIPE_BIN = BIN_DIR / "rustypipe-botguard"

DOWNLOADS_DIR = BASE_DIR / "downloads"
DOWNLOADS_DIR.mkdir(exist_ok=True)

FFMPEG_PATH = imageio_ffmpeg.get_ffmpeg_exe()
MAX_FILESIZE_BYTES = 50 * 1024 * 1024

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)

_rustypipe_ready = False

def setup_rustypipe() -> bool:
    global _rustypipe_ready
    if _rustypipe_ready:
        return True

    if not RUSTYPIPE_BIN.exists():
        logger.warning("rustypipe-botguard topilmadi, fallback qatlamlar ishlatiladi.")
        return False

    try:
        current_mode = RUSTYPIPE_BIN.stat().st_mode
        RUSTYPIPE_BIN.chmod(current_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    except Exception:
        logger.exception("Executable huquq berishda xatolik")
        return False

    bin_dir_str = str(BIN_DIR)
    if bin_dir_str not in os.environ.get("PATH", ""):
        os.environ["PATH"] = bin_dir_str + os.pathsep + os.environ.get("PATH", "")

    _rustypipe_ready = True
    return True

_cookies_path_cache: str | None = None

def get_cookies_file() -> str | None:
    global _cookies_path_cache
    if _cookies_path_cache and os.path.exists(_cookies_path_cache):
        return _cookies_path_cache

    b64 = os.getenv("YT_COOKIES_B64")
    if not b64:
        return None

    path = os.path.join(tempfile.gettempdir(), "yt_cookies.txt")
    try:
        with open(path, "wb") as f:
            f.write(base64.b64decode(b64))
        _cookies_path_cache = path
        return path
    except Exception:
        logger.exception("Cookie decode xatosi")
        return None

def _base_opts(output_template: str, audio_only: bool) -> dict:
    opts = {
        "outtmpl": output_template,
        "ffmpeg_location": FFMPEG_PATH,
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "max_filesize": MAX_FILESIZE_BYTES,
        "http_headers": {"User-Agent": USER_AGENT},
        "retries": 3,
        "extractor_args": {
            "youtube": {"player_client": ["tv", "web_safari", "web"]},
        },
    }

    if audio_only:
        opts["format"] = "bestaudio/best"
        opts["postprocessors"] = [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ]
    else:
        opts["format"] = "bestvideo[filesize<50M]+bestaudio/best[filesize<50M]/best"
        opts["merge_output_format"] = "mp4"

    return opts

def _build_opts(output_template: str, use_cookies: bool, audio_only: bool) -> dict:
    opts = _base_opts(output_template, audio_only)
    setup_rustypipe()

    if use_cookies:
        cookies_path = get_cookies_file()
        if cookies_path:
            opts["cookiefile"] = cookies_path

    return opts

class DownloadResult:
    def __init__(self, filepath: str, title: str, ext: str):
        self.filepath = filepath
        self.title = title
        self.ext = ext

def _sync_download(url: str, audio_only: bool) -> DownloadResult:
    unique_id = uuid.uuid4().hex[:8]
    output_template = str(DOWNLOADS_DIR / f"{unique_id}_%(title).80s.%(ext)s")
    last_error: Exception | None = None

    for use_cookies in (False, True):
        opts = _build_opts(output_template, use_cookies=use_cookies, audio_only=audio_only)
        try:
            with YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filepath = ydl.prepare_filename(info)

                if audio_only:
                    base, _ = os.path.splitext(filepath)
                    mp3_path = base + ".mp3"
                    if os.path.exists(mp3_path):
                        filepath = mp3_path

                if not os.path.exists(filepath):
                    candidates = glob.glob(str(DOWNLOADS_DIR / f"{unique_id}_*"))
                    if candidates:
                        filepath = candidates[0]

                return DownloadResult(
                    filepath=filepath,
                    title=info.get("title", "media"),
                    ext=os.path.splitext(filepath)[1].lstrip("."),
                )
        except DownloadError as e:
            last_error = e
            message = str(e)
            if "Sign in to confirm" not in message and "cookies" not in message.lower():
                raise
            logger.warning("Urinish muvaffaqiyatsiz (cookies=%s): %s", use_cookies, message)
            continue

    raise RuntimeError(
        f"Media faylni yuklab bo'lmadi: {last_error}"
    )

async def download_media(url: str, audio_only: bool = False) -> DownloadResult:
    return await asyncio.to_thread(_sync_download, url, audio_only)

def cleanup_file(filepath: str) -> None:
    try:
        if filepath and os.path.exists(filepath):
            os.remove(filepath)
    except Exception:
        logger.exception("Faylni o'chirishda xatolik: %s", filepath)