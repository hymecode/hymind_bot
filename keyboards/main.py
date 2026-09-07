# keyboards/main.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_language_keyboard():
    """Til tanlash tugmalari"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🇺🇿 O'zbekcha")],
            [KeyboardButton(text="🇬🇧 English")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def get_main_keyboard(lang: str = "uz"):
    """Asosiy menyu (tilga qarab)"""
    if lang == "uz":
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🌍 Tarjima")],
                [KeyboardButton(text="📝 Tests"), KeyboardButton(text="🆘 Support")],
                [KeyboardButton(text="🎬 Media")]
            ],
            resize_keyboard=True,
            one_time_keyboard=False
        )
    else:
        # English version
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🌍 Translate")],
                [KeyboardButton(text="📝 Tests"), KeyboardButton(text="🆘 Support")],
                [KeyboardButton(text="🎬 Media")]
            ],
            resize_keyboard=True,
            one_time_keyboard=False
        )