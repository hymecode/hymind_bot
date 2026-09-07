# handlers/media.py

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from media_ids import UZB_MEDIA, ENG_MEDIA
from handlers.start import show_main_menu
from handlers.language_state import get_language

router = Router()

class MediaState(StatesGroup):
    language = State()
    category = State()

def get_text(lang: str):
    if lang == "uz":
        return {
            "menu": "🎬 **Media bo'limi**\n\nTilni tanlang:",
            "uzb": "🇺🇿 O'zbekcha",
            "eng": "🇬🇧 English",
            "back": "🔙 Asosiy menyu",
            "movies": "🎥 Filmlar",
            "cartoons": "🖌 Multfilmlar",
            "anime": "🎌 Animelar",
            "lang_selected": "📂 **{lang}** tili tanlandi.\n\nKategoriyani tanlang:",
            "no_content": "❌ Bu kategoriyada kontent topilmadi.",
            "list_title": "📂 **{category}**\n\nJami: {count} ta kontent.",
            "sent": "✅ {title} yuborildi!",
            "not_found": "❌ Kontent topilmadi!",
            "back_btn": "🔙 Orqaga"
        }
    else:
        return {
            "menu": "🎬 **Media section**\n\nChoose language:",
            "uzb": "🇺🇿 Uzbek",
            "eng": "🇬🇧 English",
            "back": "🔙 Main Menu",
            "movies": "🎥 Movies",
            "cartoons": "🖌 Cartoons",
            "anime": "🎌 Anime",
            "lang_selected": "📂 **{lang}** selected.\n\nChoose category:",
            "no_content": "❌ No content found in this category.",
            "list_title": "📂 **{category}**\n\nTotal: {count} items.",
            "sent": "✅ {title} sent!",
            "not_found": "❌ Content not found!",
            "back_btn": "🔙 Back"
        }

@router.message(F.text == "🎬 Media")
async def media_menu(message: types.Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    lang = get_language(user_id) or "uz"
    t = get_text(lang)
    
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text=t["uzb"])],
            [types.KeyboardButton(text=t["eng"])],
            [types.KeyboardButton(text=t["back"])]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    await message.answer(
        t["menu"],
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.message(F.text.in_(["🇺🇿 O'zbekcha", "🇺🇿 Uzbek", "🇬🇧 English", "🇬🇧 English"]))
async def choose_language_media(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_language(user_id) or "uz"
    t = get_text(lang)
    
    if message.text in ["🇺🇿 O'zbekcha", "🇺🇿 Uzbek"]:
        lang_code = "uzb"
        lang_display = "O'zbekcha"
    else:
        lang_code = "eng"
        lang_display = "English"
    
    await state.update_data(language=lang_code)
    await state.set_state(MediaState.category)
    
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text=t["movies"])],
            [types.KeyboardButton(text=t["cartoons"])],
            [types.KeyboardButton(text=t["anime"])],
            [types.KeyboardButton(text=t["back_btn"])]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    await message.answer(
        t["lang_selected"].format(lang=lang_display),
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.message(MediaState.category, F.text == "🔙 Orqaga")
async def back_to_media_language(message: types.Message, state: FSMContext):
    await state.clear()
    await media_menu(message, state)

@router.message(MediaState.category, F.text == "🔙 Back")
async def back_to_media_language_en(message: types.Message, state: FSMContext):
    await state.clear()
    await media_menu(message, state)

@router.message(MediaState.category, F.text.in_(["🎥 Filmlar", "🎥 Movies"]))
async def show_movies(message: types.Message, state: FSMContext):
    await show_media_list(message, state, "movies")

@router.message(MediaState.category, F.text.in_(["🖌 Multfilmlar", "🖌 Cartoons"]))
async def show_cartoons(message: types.Message, state: FSMContext):
    await show_media_list(message, state, "cartoons")

@router.message(MediaState.category, F.text.in_(["🎌 Animelar", "🎌 Anime"]))
async def show_anime(message: types.Message, state: FSMContext):
    await show_media_list(message, state, "anime")

async def show_media_list(message: types.Message, state: FSMContext, category: str):
    user_id = message.from_user.id
    lang = get_language(user_id) or "uz"
    t = get_text(lang)
    
    data = await state.get_data()
    lang_code = data.get("language", "uzb")
    
    media_data = UZB_MEDIA if lang_code == "uzb" else ENG_MEDIA
    items = media_data.get(category, [])
    
    if not items:
        await message.answer(t["no_content"])
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    category_names = {
        "movies": t["movies"],
        "cartoons": t["cartoons"],
        "anime": t["anime"]
    }
    for i, item in enumerate(items):
        title = item.get("title", f"{category_names.get(category, category)} {i+1}")
        keyboard.inline_keyboard.append(
            [InlineKeyboardButton(text=title, callback_data=f"media_{lang_code}_{category}_{i}")]
        )
    keyboard.inline_keyboard.append(
        [InlineKeyboardButton(text=t["back_btn"], callback_data="back_to_media_categories")]
    )
    
    await message.answer(
        t["list_title"].format(category=category_names.get(category, category), count=len(items)),
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.callback_query(F.data.startswith("media_"))
async def send_media(callback: types.CallbackQuery):
    data = callback.data.split("_")
    lang_code = data[1]
    category = data[2]
    index = int(data[3])
    
    media_data = UZB_MEDIA if lang_code == "uzb" else ENG_MEDIA
    items = media_data.get(category, [])
    
    user_id = callback.from_user.id
    lang = get_language(user_id) or "uz"
    t = get_text(lang)
    
    if index >= len(items):
        await callback.answer(t["not_found"], show_alert=True)
        return
    
    item = items[index]
    try:
        await callback.message.bot.copy_message(
            chat_id=callback.message.chat.id,
            from_chat_id=item['chat_id'],
            message_id=item['message_id']
        )
        await callback.answer(t["sent"].format(title=item.get('title', 'Kontent')))
    except Exception as e:
        await callback.answer(f"❌ Xatolik: {e}", show_alert=True)

@router.callback_query(F.data == "back_to_media_categories")
async def back_to_categories(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    user_id = callback.from_user.id
    lang = get_language(user_id) or "uz"
    t = get_text(lang)
    
    data = await state.get_data()
    lang_code = data.get("language", "uzb")
    lang_display = "O'zbekcha" if lang_code == "uzb" else "English"
    
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text=t["movies"])],
            [types.KeyboardButton(text=t["cartoons"])],
            [types.KeyboardButton(text=t["anime"])],
            [types.KeyboardButton(text=t["back_btn"])]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    await callback.message.answer(
        t["lang_selected"].format(lang=lang_display),
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await callback.answer()

# Asosiy menyuga qaytish
@router.message(F.text == "🔙 Asosiy menyu")
async def back_to_main_media_uz(message: types.Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    lang = get_language(user_id) or "uz"
    await show_main_menu(message, lang)

@router.message(F.text == "🔙 Main Menu")
async def back_to_main_media_en(message: types.Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    lang = get_language(user_id) or "en"
    await show_main_menu(message, lang)