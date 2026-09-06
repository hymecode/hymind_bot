from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🌍 Tarjima"), KeyboardButton(text="🎲 Randoms")],
            [KeyboardButton(text="🍅 Pomodoro"), KeyboardButton(text="⭐ Premium")],
            [KeyboardButton(text="🎁 Promo-kod")],
            [KeyboardButton(text="🆘 Support"), KeyboardButton(text="👤 Profil")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False 
    )