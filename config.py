import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN topilmadi! .env faylini tekshiring.")

# Admin ID'lari (o'zingizning Telegram ID'ngizni yozing)
ADMIN_IDS = [8896470319]  # O'z ID'ngiz bilan almashtiring!

ADMIN_USERNAME = "@hymecode"  # @ belgisiz
DONATE_CARD = "6262570191961988"  # Karta raqami
OFFERS_CHAT_ID = -1004359574809 # Takliflar uchun yopiq guruh ID