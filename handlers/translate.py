from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from deep_translator import GoogleTranslator
from keyboards.translate import get_translate_keyboard, get_back_keyboard

router = Router()

# FSM holati
class TranslateState(StatesGroup):
    waiting_text = State()

@router.message(F.text == "🌍 Tarjima")
async def translate_menu(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "🌍 Tarjima bo'limi\n\n"
        "Yo'nalishni tanlang va matn yuboring:",
        reply_markup=get_translate_keyboard()
    )

@router.message(F.text.in_(["🇬🇧 Eng → Uzb 🇺🇿", "🇺🇿 Uzb → Eng 🇬🇧"]))
async def choose_lang(message: types.Message, state: FSMContext):
    direction = "en-uz" if message.text == "🇬🇧 Eng → Uzb 🇺🇿" else "uz-en"
    await state.update_data(direction=direction)
    await state.set_state(TranslateState.waiting_text)
    
    await message.answer(
        f"✅ {message.text} rejimi yoqildi.\n"
        "Endi matn yuboring yoki 🔙 Orqaga bosing.",
        reply_markup=get_back_keyboard()
    )

@router.message(TranslateState.waiting_text, F.text == "🔙 Orqaga")
async def back_from_translate(message: types.Message, state: FSMContext):
    await state.clear()
    await translate_menu(message, state)

@router.message(TranslateState.waiting_text, F.text)
async def translate_text(message: types.Message, state: FSMContext):
    data = await state.get_data()
    direction = data.get("direction", "en-uz")
    text = message.text
    
    try:
        if direction == "en-uz":
            result = GoogleTranslator(source='en', target='uz').translate(text)
        else:
            result = GoogleTranslator(source='uz', target='en').translate(text)
        await message.answer(f"🔹 **Tarjima:**\n{result}", parse_mode="Markdown")
    except Exception as e:
        await message.answer(f"❌ Xatolik yuz berdi: {e}\nQayta urinib ko'ring.")

# Asosiy menyuga qaytish
@router.message(F.text == "🔙 Asosiy menyu")
async def back_to_main(message: types.Message, state: FSMContext):
    await state.clear()
    from handlers.start import cmd_start
    await cmd_start(message)