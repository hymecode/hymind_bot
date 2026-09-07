# handlers/translate.py

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from deep_translator import GoogleTranslator
from handlers.language_state import get_language
from handlers.start import show_main_menu

router = Router()

class TranslateState(StatesGroup):
    waiting_text = State()

# Tarjima tugmalari ro‘yxati
TRANSLATE_BUTTONS = [
    "🇺🇿 O'zbekcha", "🇷🇺 Ruscha", "🇬🇧 English",
    "🇺🇿 Uzbek", "🇷🇺 Russian",
    "🔙 Asosiy menyu", "🔙 Main Menu",
    "🔙 Orqaga", "🔙 Back"
]

def get_translate_keyboard(lang: str = "uz"):
    if lang == "uz":
        return types.ReplyKeyboardMarkup(
            keyboard=[
                [types.KeyboardButton(text="🇺🇿 O'zbekcha")],
                [types.KeyboardButton(text="🇷🇺 Ruscha")],
                [types.KeyboardButton(text="🇬🇧 English")],
                [types.KeyboardButton(text="🔙 Asosiy menyu")]
            ],
            resize_keyboard=True,
            one_time_keyboard=False
        )
    else:
        return types.ReplyKeyboardMarkup(
            keyboard=[
                [types.KeyboardButton(text="🇺🇿 Uzbek")],
                [types.KeyboardButton(text="🇷🇺 Russian")],
                [types.KeyboardButton(text="🇬🇧 English")],
                [types.KeyboardButton(text="🔙 Main Menu")]
            ],
            resize_keyboard=True,
            one_time_keyboard=False
        )

@router.message(F.text == "🌍 Tarjima")
async def translate_menu(message: types.Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    lang = get_language(user_id) or "uz"
    
    if lang == "uz":
        text = "🌍 **Tarjima**\n\nMatn yoki so'z yuboring, men uni tarjima qilaman:"
    else:
        text = "🌍 **Translate**\n\nSend a text or word, I will translate it:"
    
    await state.set_state(TranslateState.waiting_text)
    await message.answer(
        text,
        reply_markup=types.ReplyKeyboardRemove(),
        parse_mode="Markdown"
    )

# Matn qabul qilish (faqat matn, tugmalar EMAS)
@router.message(TranslateState.waiting_text, F.text, ~F.text.in_(TRANSLATE_BUTTONS))
async def receive_text(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    lang = get_language(user_id) or "uz"
    text = message.text
    
    await state.update_data(text=text)
    
    if lang == "uz":
        prompt = "✅ Matn qabul qilindi. Qaysi tilga tarjima qilay?"
    else:
        prompt = "✅ Text received. Which language to translate to?"
    
    await message.answer(
        prompt,
        reply_markup=get_translate_keyboard(lang)
    )

# ========== TARJIMA TUGMALARI ==========

@router.message(F.text.in_(["🇺🇿 O'zbekcha", "🇺🇿 Uzbek"]))
async def translate_to_uzbek(message: types.Message, state: FSMContext):
    await translate_to_language(message, state, "uz")

@router.message(F.text.in_(["🇷🇺 Ruscha", "🇷🇺 Russian"]))
async def translate_to_russian(message: types.Message, state: FSMContext):
    await translate_to_language(message, state, "ru")

@router.message(F.text.in_(["🇬🇧 English", "🇬🇧 English"]))
async def translate_to_english(message: types.Message, state: FSMContext):
    await translate_to_language(message, state, "en")

async def translate_to_language(message: types.Message, state: FSMContext, target_lang: str):
    user_id = message.from_user.id
    lang = get_language(user_id) or "uz"
    
    data = await state.get_data()
    text = data.get("text")
    
    if not text:
        await message.answer("❌ Matn topilmadi. Iltimos, qayta matn yuboring.")
        await state.clear()
        return
    
    try:
        translator = GoogleTranslator(source='auto', target=target_lang)
        result = translator.translate(text)
        
        lang_names = {
            "uz": "🇺🇿 O'zbekcha",
            "ru": "🇷🇺 Ruscha",
            "en": "🇬🇧 English"
        }
        
        if lang == "uz":
            await message.answer(
                f"🔹 **Tarjima ({lang_names.get(target_lang, target_lang)}):**\n\n{result}",
                parse_mode="Markdown"
            )
            await message.answer(
                "📝 Yana matn yuboring yoki 🔙 Asosiy menyu ga qayting.",
                reply_markup=get_translate_keyboard(lang)
            )
        else:
            await message.answer(
                f"🔹 **Translation ({lang_names.get(target_lang, target_lang)}):**\n\n{result}",
                parse_mode="Markdown"
            )
            await message.answer(
                "📝 Send another text or go 🔙 Main Menu.",
                reply_markup=get_translate_keyboard(lang)
            )
        
        await state.update_data(text=None)
        
    except Exception as e:
        if lang == "uz":
            await message.answer(f"❌ Xatolik: {e}\nQayta urinib ko'ring.")
        else:
            await message.answer(f"❌ Error: {e}\nTry again.")

# ========== ASOSIY MENYUGA QAYTISH ==========

@router.message(F.text == "🔙 Asosiy menyu")
async def back_to_main_translate_uz(message: types.Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    lang = get_language(user_id) or "uz"
    await show_main_menu(message, lang)

@router.message(F.text == "🔙 Main Menu")
async def back_to_main_translate_en(message: types.Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    lang = get_language(user_id) or "en"
    await show_main_menu(message, lang)