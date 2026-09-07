from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.main import (
    language_select_kb,
    main_menu_kb,
    BTN_LANG_UZ,
    BTN_LANG_EN,
    BTN_BACK,
)
from handlers.language_state import set_language, get_language, has_language

router = Router(name="start")

WELCOME_TEXTS = {
    "uz": "🎉 Botga xush kelibsiz!\n\nAsosiy menyudan kerakli bo'limni tanlang:",
    "en": "🎉 Welcome to the bot!\n\nPlease choose a section from the main menu:",
}


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    user_id = message.from_user.id

    if has_language(user_id):
        lang = get_language(user_id)
        await message.answer(
            WELCOME_TEXTS.get(lang, WELCOME_TEXTS["uz"]),
            reply_markup=main_menu_kb(),
        )
        return

    await message.answer(
        "🌐 Tilni tanlang / Please choose your language:",
        reply_markup=language_select_kb(),
    )


@router.message(F.text == BTN_LANG_UZ)
async def choose_lang_uz(message: Message) -> None:
    set_language(message.from_user.id, "uz")
    await message.answer(WELCOME_TEXTS["uz"], reply_markup=main_menu_kb())


@router.message(F.text == BTN_LANG_EN)
async def choose_lang_en(message: Message) -> None:
    set_language(message.from_user.id, "en")
    await message.answer(WELCOME_TEXTS["en"], reply_markup=main_menu_kb())


@router.message(F.text == BTN_BACK)
async def back_to_main_menu(message: Message) -> None:
    """
    Har qanday bo'limdan "🔙 Asosiy menyu" tugmasi bosilganda ishlaydi.
    Bu handler eng oxirida ro'yxatdan o'tkazilishi kerak (main.py dagi
    tartibga qarang), aks holda boshqa bo'limlardagi FSM holatlarini
    "yutib" yuborishi mumkin. Lekin FSM state clear qilingani uchun
    xavfsiz - state cleardan keyingina bu yerga tushadi.
    """
    user_id = message.from_user.id
    if not has_language(user_id):
        await message.answer(
            "🌐 Tilni tanlang / Please choose your language:",
            reply_markup=language_select_kb(),
        )
        return

    lang = get_language(user_id)
    await message.answer(WELCOME_TEXTS.get(lang, WELCOME_TEXTS["uz"]), reply_markup=main_menu_kb())
