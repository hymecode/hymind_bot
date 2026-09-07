import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# O'zingizning Telegram ID'ingizni shu yerga qo'shing
ADMIN_IDS = [8896470319]

# Qo'llab-quvvatlash uchun karta raqami va admin username
SUPPORT_CARD_NUMBER = "6262 5701 9196 1988"
ADMIN_USERNAME = "@hymecode"

if not BOT_TOKEN:
    raise ValueError(
        "BOT_TOKEN topilmadi! .env faylida BOT_TOKEN=... qiymatini kiriting."
    )
