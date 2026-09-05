from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_translate_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🇬🇧 Eng → Uzb 🇺🇿")],
            [KeyboardButton(text="🇺🇿 Uzb → Eng 🇬🇧")],
            [KeyboardButton(text="🔙 Asosiy menyu")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )

def get_back_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔙 Orqaga")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )