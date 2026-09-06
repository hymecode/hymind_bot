from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🌍 Tarjima")],
            [KeyboardButton(text="📝 Tests"), KeyboardButton(text="🎬 Media")],
            [KeyboardButton(text="🆘 Support")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )