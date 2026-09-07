from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from deep_translator import GoogleTranslator

from keyboards.main import (
    remove_keyboard,
    translate_lang_kb,
    main_menu_kb,
    BTN_TRANSLATE,
    BTN_BACK,
    BTN_TR_UZ,
    BTN_TR_RU,
    BTN_TR_EN,
)
from handlers.language_state import get_language

router = Router(name="translate")

LANG_CODE_MAP = {
    BTN_TR_UZ: "uz",
    BTN_TR_RU: "ru",
    BTN_TR_EN: "en",
}


class TranslateStates(StatesGroup):
    waiting_for_text = State()
    waiting_for_language = State()


ASK_TEXT_MSG = "✍️ Tarjima qilinadigan matnni yuboring:"


@router.message(F.text == BTN_TRANSLATE)
async def start_translate(message: Message, state: FSMContext) -> None:
    await state.set_state(TranslateStates.waiting_for_text)
    await message.answer(ASK_TEXT_MSG, reply_markup=remove_keyboard())


@router.message(TranslateStates.waiting_for_text, F.text == BTN_BACK)
async def back_from_waiting_text(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("🔙 Asosiy menyu", reply_markup=main_menu_kb())


@router.message(TranslateStates.waiting_for_text, F.text)
async def receive_text_to_translate(message: Message, state: FSMContext) -> None:
    await state.update_data(source_text=message.text)
    await state.set_state(TranslateStates.waiting_for_language)
    await message.answer(
        "🈯 Qaysi tilga tarjima qilinsin?",
        reply_markup=translate_lang_kb(),
    )


@router.message(TranslateStates.waiting_for_language, F.text == BTN_BACK)
async def back_from_waiting_language(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("🔙 Asosiy menyu", reply_markup=main_menu_kb())


@router.message(TranslateStates.waiting_for_language, F.text.in_(LANG_CODE_MAP.keys()))
async def do_translate(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    source_text = data.get("source_text", "")
    target_lang = LANG_CODE_MAP[message.text]

    try:
        translated = GoogleTranslator(source="auto", target=target_lang).translate(source_text)
    except Exception as e:
        await message.answer(f"⚠️ Tarjima qilishda xatolik yuz berdi: {e}")
        translated = None

    if translated:
        await message.answer(f"✅ Natija:\n\n{translated}")

    # Yana matn kiritishni so'raymiz (klaviatura tozalanadi)
    await state.set_state(TranslateStates.waiting_for_text)
    await message.answer(ASK_TEXT_MSG, reply_markup=remove_keyboard())
