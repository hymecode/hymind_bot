from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from media_ids import UZB_MEDIA, ENG_MEDIA

router = Router()

class MediaState(StatesGroup):
    language = State()
    category = State()

# ========== ASOSIY MENYU ==========

@router.message(F.text == "🎬 Media")
async def media_menu(message: types.Message, state: FSMContext):
    await state.clear()
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="🇺🇿 O'zbekcha")],
            [types.KeyboardButton(text="🇬🇧 English")],
            [types.KeyboardButton(text="🔙 Asosiy menyu")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    await message.answer(
        "🎬 **Media bo'limi**\n\n"
        "Tilni tanlang:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

# ========== TIL TANLASH ==========

@router.message(F.text.in_(["🇺🇿 O'zbekcha", "🇬🇧 English"]))
async def choose_language(message: types.Message, state: FSMContext):
    lang = "uzb" if message.text == "🇺🇿 O'zbekcha" else "eng"
    await state.update_data(language=lang)
    await state.set_state(MediaState.category)
    
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="🎥 Filmlar")],
            [types.KeyboardButton(text="🖌 Multfilmlar")],
            [types.KeyboardButton(text="🎌 Animelar")],
            [types.KeyboardButton(text="🔙 Orqaga")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    await message.answer(
        f"📂 **{message.text}** tili tanlandi.\n\n"
        "Kategoriyani tanlang:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.message(F.text == "🔙 Orqaga", MediaState.category)
async def back_to_media_language(message: types.Message, state: FSMContext):
    await state.clear()
    await media_menu(message, state)

# ========== KATEGORIYA TANLASH ==========

@router.message(MediaState.category, F.text == "🎥 Filmlar")
async def show_movies(message: types.Message, state: FSMContext):
    await show_media_list(message, state, "movies")

@router.message(MediaState.category, F.text == "🖌 Multfilmlar")
async def show_cartoons(message: types.Message, state: FSMContext):
    await show_media_list(message, state, "cartoons")

@router.message(MediaState.category, F.text == "🎌 Animelar")
async def show_anime(message: types.Message, state: FSMContext):
    await show_media_list(message, state, "anime")

async def show_media_list(message: types.Message, state: FSMContext, category: str):
    data = await state.get_data()
    lang = data.get("language", "uzb")
    
    media_data = UZB_MEDIA if lang == "uzb" else ENG_MEDIA
    items = media_data.get(category, [])
    
    if not items:
        await message.answer("❌ Bu kategoriyada kontent topilmadi.")
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for i, item in enumerate(items):
        title = item.get("title", f"{category.capitalize()} {i+1}")
        keyboard.inline_keyboard.append(
            [InlineKeyboardButton(text=title, callback_data=f"media_{lang}_{category}_{i}")]
        )
    keyboard.inline_keyboard.append(
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_media_categories")]
    )
    
    await message.answer(
        f"📂 **{category.capitalize()}**\n\nJami: {len(items)} ta kontent.",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

# ========== KONTENTNI YUBORISH ==========

@router.callback_query(F.data.startswith("media_"))
async def send_media(callback: types.CallbackQuery):
    data = callback.data.split("_")
    lang = data[1]  # uzb yoki eng
    category = data[2]  # movies, cartoons, anime
    index = int(data[3])
    
    media_data = UZB_MEDIA if lang == "uzb" else ENG_MEDIA
    items = media_data.get(category, [])
    
    if index >= len(items):
        await callback.answer("❌ Kontent topilmadi!", show_alert=True)
        return
    
    item = items[index]
    try:
        await callback.message.bot.copy_message(
            chat_id=callback.message.chat.id,
            from_chat_id=item['chat_id'],
            message_id=item['message_id']
        )
        await callback.answer(f"✅ {item.get('title', 'Kontent')} yuborildi!")
    except Exception as e:
        await callback.answer(f"❌ Xatolik: {e}", show_alert=True)

# ========== ORQAGA QAYTISH ==========

@router.callback_query(F.data == "back_to_media_categories")
async def back_to_categories(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    # Tilni saqlab qolgan holda kategoriya menyusini ko'rsatish
    data = await state.get_data()
    lang = data.get("language", "uzb")
    lang_text = "🇺🇿 O'zbekcha" if lang == "uzb" else "🇬🇧 English"
    
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="🎥 Filmlar")],
            [types.KeyboardButton(text="🖌 Multfilmlar")],
            [types.KeyboardButton(text="🎌 Animelar")],
            [types.KeyboardButton(text="🔙 Orqaga")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    await callback.message.answer(
        f"📂 **{lang_text}** tili tanlandi.\n\n"
        "Kategoriyani tanlang:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await callback.answer()

# ========== ASOSIY MENYUGA QAYTISH ==========

@router.message(F.text == "🔙 Asosiy menyu")
async def back_to_main_media(message: types.Message, state: FSMContext):
    await state.clear()
    from handlers.start import cmd_start
    await cmd_start(message)