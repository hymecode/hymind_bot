from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.main import (
    media_lang_kb,
    media_category_kb,
    media_list_kb,
    main_menu_kb,
    BTN_MEDIA,
    BTN_BACK,
    BTN_LANG_UZ,
    BTN_LANG_EN,
    BTN_MEDIA_MOVIES,
    BTN_MEDIA_CARTOONS,
    BTN_MEDIA_ANIME,
    BTN_MEDIA_MOVIES_EN,
    BTN_MEDIA_CARTOONS_EN,
    BTN_MEDIA_ANIME_EN,
)
from media_ids import UZB_MEDIA, ENG_MEDIA

router = Router(name="media")

CATEGORY_BUTTON_MAP = {
    BTN_MEDIA_MOVIES: "movies",
    BTN_MEDIA_CARTOONS: "cartoons",
    BTN_MEDIA_ANIME: "anime",
    BTN_MEDIA_MOVIES_EN: "movies",
    BTN_MEDIA_CARTOONS_EN: "cartoons",
    BTN_MEDIA_ANIME_EN: "anime",
}


class MediaStates(StatesGroup):
    choosing_language = State()
    choosing_category = State()
    choosing_content = State()


@router.message(F.text == BTN_MEDIA)
async def open_media_menu(message: Message, state: FSMContext) -> None:
    await state.set_state(MediaStates.choosing_language)
    await message.answer("🌐 Tilni tanlang:", reply_markup=media_lang_kb())


@router.message(MediaStates.choosing_language, F.text == BTN_BACK)
async def back_from_media_lang(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("🔙 Asosiy menyu", reply_markup=main_menu_kb())


@router.message(MediaStates.choosing_language, F.text.in_({BTN_LANG_UZ, BTN_LANG_EN}))
async def choose_media_language(message: Message, state: FSMContext) -> None:
    lang = "uz" if message.text == BTN_LANG_UZ else "en"
    await state.update_data(media_lang=lang)
    await state.set_state(MediaStates.choosing_category)
    await message.answer("🎬 Kategoriyani tanlang:", reply_markup=media_category_kb(lang))


@router.message(MediaStates.choosing_category, F.text == BTN_BACK)
async def back_from_media_category(message: Message, state: FSMContext) -> None:
    await state.set_state(MediaStates.choosing_language)
    await message.answer("🌐 Tilni tanlang:", reply_markup=media_lang_kb())


@router.message(MediaStates.choosing_category, F.text.in_(CATEGORY_BUTTON_MAP.keys()))
async def choose_media_category(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get("media_lang", "uz")
    category = CATEGORY_BUTTON_MAP[message.text]
    source = UZB_MEDIA if lang == "uz" else ENG_MEDIA
    content_list = source.get(category, [])

    if not content_list:
        await message.answer("😔 Hozircha bu kategoriyada kontent mavjud emas.")
        return

    titles = [c["title"] for c in content_list]
    await state.update_data(category=category)
    await state.set_state(MediaStates.choosing_content)
    await message.answer("📋 Kontentni tanlang:", reply_markup=media_list_kb(titles))


@router.message(MediaStates.choosing_content, F.text == BTN_BACK)
async def back_from_media_content(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get("media_lang", "uz")
    await state.set_state(MediaStates.choosing_category)
    await message.answer("🎬 Kategoriyani tanlang:", reply_markup=media_category_kb(lang))


@router.message(MediaStates.choosing_content, F.text)
async def send_selected_content(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get("media_lang", "uz")
    category = data.get("category")
    source = UZB_MEDIA if lang == "uz" else ENG_MEDIA
    content_list = source.get(category, [])

    selected = next((c for c in content_list if c["title"] == message.text), None)
    if not selected:
        await message.answer("⚠️ Bunday kontent topilmadi, ro'yxatdan tanlang.")
        return

    try:
        await message.bot.copy_message(
            chat_id=message.chat.id,
            from_chat_id=selected["chat_id"],
            message_id=selected["message_id"],
        )
    except Exception as e:
        await message.answer(f"⚠️ Kontentni yuborishda xatolik: {e}")