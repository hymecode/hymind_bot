import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN topilmadi! .env faylini tekshiring.")

# Admin ID lari (o'zingiz va ishonchli odamlarniki)
ADMIN_IDS = [8896470319]  # O'ZINGIZNING TELEGRAM ID'NGIZNI YOZING!