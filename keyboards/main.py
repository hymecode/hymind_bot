from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🌍 Tarjima")],
            [KeyboardButton(text="🍅 Pomodoro"), KeyboardButton(text="⭐ Premium")],
            [KeyboardButton(text="🎲 Randoms"), KeyboardButton(text="🎁 Promo-kod")],
            [KeyboardButton(text="👤 Profil")]
            [KeyboardButton(text="🆘 Support")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )