from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from handlers.language_state import set_language, get_language
from keyboards.main import get_main_keyboard, get_language_keyboard

router = Router()

class LanguageState(StatesGroup):
    choosing_language = State()

@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    
    lang = get_language(user_id)
    
    if lang is None:
        await state.set_state(LanguageState.choosing_language)
        await message.answer(
            "🌍 Tilni tanlang / Choose language:",
            reply_markup=get_language_keyboard()
        )
        return
    
    await show_main_menu(message, lang)

@router.message(LanguageState.choosing_language, F.text.in_(["🇺🇿 O'zbekcha", "🇬🇧 English"]))
async def choose_language(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    lang = "uz" if message.text == "🇺🇿 O'zbekcha" else "en"
    
    set_language(user_id, lang)
    await state.clear()
    
    await show_main_menu(message, lang)

async def show_main_menu(message: types.Message, lang: str):
    if lang == "uz":
        text = "🧠 **HyMind** botiga xush kelibsiz!\n\nQuyidagi bo'limlardan birini tanlang:"
    else:
        text = "🧠 **HyMind** botiga xush kelibsiz!\n\nChoose one of the following sections:"
    
    await message.answer(
        text,
        reply_markup=get_main_keyboard(lang),
        parse_mode="Markdown"
    )