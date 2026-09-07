# handlers/tests.py

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from test_ids import IELTS_TESTS, SAT_TESTS
from handlers.start import show_main_menu
from handlers.language_state import get_language

router = Router()

def get_text(lang: str, key: str):
    texts = {
        "uz": {
            "menu": "📝 **Tests bo'limi**\n\nQuyidagi tugmalardan birini tanlang:",
            "ielts": "📚 IELTS",
            "sat": "📚 SAT",
            "back": "🔙 Asosiy menyu",
            "no_tests": "❌ {category} testlari topilmadi.",
            "list_title": "📚 **{category} testlari**\n\nJami: {count} ta test.",
            "sent": "✅ Test {num} yuborildi!",
            "not_found": "❌ Bunday test mavjud emas!"
        },
        "en": {
            "menu": "📝 **Tests section**\n\nChoose one of the following:",
            "ielts": "📚 IELTS",
            "sat": "📚 SAT",
            "back": "🔙 Main Menu",
            "no_tests": "❌ No {category} tests found.",
            "list_title": "📚 **{category} tests**\n\nTotal: {count} tests.",
            "sent": "✅ Test {num} sent!",
            "not_found": "❌ Test not found!"
        }
    }
    return texts.get(lang, texts["uz"]).get(key, "")

@router.message(F.text == "📝 Tests")
async def tests_menu(message: types.Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    lang = get_language(user_id) or "uz"
    
    t = get_text(lang, "")
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text=t.get("ielts", "📚 IELTS"))],
            [types.KeyboardButton(text=t.get("sat", "📚 SAT"))],
            [types.KeyboardButton(text=t.get("back", "🔙 Asosiy menyu"))]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    await message.answer(
        get_text(lang, "menu"),
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.message(F.text == "📚 IELTS")
async def show_ielts_tests(message: types.Message):
    await show_test_list(message, IELTS_TESTS, "IELTS")

@router.message(F.text == "📚 SAT")
async def show_sat_tests(message: types.Message):
    await show_test_list(message, SAT_TESTS, "SAT")

async def show_test_list(message: types.Message, tests: list, category: str):
    user_id = message.from_user.id
    lang = get_language(user_id) or "uz"
    t = get_text(lang, "")
    
    if not tests:
        await message.answer(t.get("no_tests", "").format(category=category))
        return

    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for i in range(len(tests)):
        keyboard.inline_keyboard.append(
            [InlineKeyboardButton(text=f"Test {i+1}", callback_data=f"test_{category.lower()}_{i}")]
        )
    keyboard.inline_keyboard.append(
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_tests")]
    )

    await message.answer(
        t.get("list_title", "").format(category=category, count=len(tests)),
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.callback_query(F.data.startswith("test_"))
async def send_test(callback: types.CallbackQuery):
    data = callback.data.split("_")
    category = data[1]
    index = int(data[2])

    tests = IELTS_TESTS if category == "ielts" else SAT_TESTS
    user_id = callback.from_user.id
    lang = get_language(user_id) or "uz"
    t = get_text(lang, "")
    
    if index >= len(tests):
        await callback.answer(t.get("not_found", ""), show_alert=True)
        return

    test = tests[index]
    try:
        await callback.message.bot.copy_message(
            chat_id=callback.message.chat.id,
            from_chat_id=test['chat_id'],
            message_id=test['message_id']
        )
        await callback.answer(t.get("sent", "").format(num=index+1))
    except Exception as e:
        await callback.answer(f"❌ Xatolik: {e}", show_alert=True)

@router.callback_query(F.data == "back_to_tests")
async def back_to_tests(callback: types.CallbackQuery):
    await callback.message.delete()
    await tests_menu(callback.message, None)
    await callback.answer()

# Asosiy menyuga qaytish
@router.message(F.text == "🔙 Asosiy menyu")
async def back_to_main_tests_uz(message: types.Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    lang = get_language(user_id) or "uz"
    await show_main_menu(message, lang)

@router.message(F.text == "🔙 Main Menu")
async def back_to_main_tests_en(message: types.Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    lang = get_language(user_id) or "en"
    await show_main_menu(message, lang)