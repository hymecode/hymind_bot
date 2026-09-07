from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# ---------- Umumiy tugmalar matni ----------
BTN_BACK = "🔙 Asosiy menyu"

BTN_LANG_UZ = "🇺🇿 O'zbek"
BTN_LANG_EN = "🇬🇧 English"

BTN_TRANSLATE = "🌍 Tarjima"
BTN_TESTS = "📝 Tests"
BTN_SUPPORT = "🆘 Support"
BTN_MEDIA = "🎬 Media"

BTN_TR_UZ = "Oʻzbekcha"
BTN_TR_RU = "Ruscha"
BTN_TR_EN = "English"

BTN_TEST_IELTS = "📚 IELTS"
BTN_TEST_SAT = "📚 SAT"

BTN_MEDIA_MOVIES = "🎥 Filmlar"
BTN_MEDIA_CARTOONS = "🧸 Multfilmlar"
BTN_MEDIA_ANIME = "🀄 Animelar"

BTN_MEDIA_MOVIES_EN = "🎥 Movies"
BTN_MEDIA_CARTOONS_EN = "🧸 Cartoons"
BTN_MEDIA_ANIME_EN = "🀄 Anime"

BTN_SUPPORT_ADMIN = "👤 Admin"
BTN_SUPPORT_SUGGEST = "✍️ Taklif yozish"
BTN_SUPPORT_DONATE = "💳 Qoʻllab-quvvatlash"


def remove_keyboard() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()


def language_select_kb() -> ReplyKeyboardMarkup:
    """Bot birinchi marta ishga tushganda / restartdan keyin til tanlash klaviaturasi."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_LANG_UZ), KeyboardButton(text=BTN_LANG_EN)],
        ],
        resize_keyboard=True,
    )


def main_menu_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_TRANSLATE), KeyboardButton(text=BTN_TESTS)],
            [KeyboardButton(text=BTN_SUPPORT), KeyboardButton(text=BTN_MEDIA)],
        ],
        resize_keyboard=True,
    )


def back_only_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=BTN_BACK)]],
        resize_keyboard=True,
    )


def translate_lang_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=BTN_TR_UZ),
                KeyboardButton(text=BTN_TR_RU),
                KeyboardButton(text=BTN_TR_EN),
            ],
            [KeyboardButton(text=BTN_BACK)],
        ],
        resize_keyboard=True,
    )


def tests_menu_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_TEST_IELTS), KeyboardButton(text=BTN_TEST_SAT)],
            [KeyboardButton(text=BTN_BACK)],
        ],
        resize_keyboard=True,
    )


def tests_list_kb(titles: list[str]) -> ReplyKeyboardMarkup:
    rows = [[KeyboardButton(text=t)] for t in titles]
    rows.append([KeyboardButton(text=BTN_BACK)])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def media_lang_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_LANG_UZ), KeyboardButton(text=BTN_LANG_EN)],
            [KeyboardButton(text=BTN_BACK)],
        ],
        resize_keyboard=True,
    )


def media_category_kb(lang: str) -> ReplyKeyboardMarkup:
    if lang == "uz":
        movies, cartoons, anime = BTN_MEDIA_MOVIES, BTN_MEDIA_CARTOONS, BTN_MEDIA_ANIME
    else:
        movies, cartoons, anime = (
            BTN_MEDIA_MOVIES_EN,
            BTN_MEDIA_CARTOONS_EN,
            BTN_MEDIA_ANIME_EN,
        )
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=movies), KeyboardButton(text=cartoons)],
            [KeyboardButton(text=anime)],
            [KeyboardButton(text=BTN_BACK)],
        ],
        resize_keyboard=True,
    )


def media_list_kb(titles: list[str]) -> ReplyKeyboardMarkup:
    rows = [[KeyboardButton(text=t)] for t in titles]
    rows.append([KeyboardButton(text=BTN_BACK)])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def support_menu_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_SUPPORT_ADMIN), KeyboardButton(text=BTN_SUPPORT_SUGGEST)],
            [KeyboardButton(text=BTN_SUPPORT_DONATE)],
            [KeyboardButton(text=BTN_BACK)],
        ],
        resize_keyboard=True,
    )
