from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from test_ids import IELTS_TESTS, SAT_TESTS

router = Router()

@router.message(F.text == "📝 Tests")
async def tests_menu(message: types.Message, state: FSMContext):
    await state.clear()
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="📚 IELTS")],
            [types.KeyboardButton(text="📚 SAT")],
            [types.KeyboardButton(text="🔙 Asosiy menyu")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    await message.answer(
        "📝 **Tests bo'limi**\n\n"
        "Quyidagi tugmalardan birini tanlang:",
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
    if not tests:
        await message.answer(f"❌ {category} testlari topilmadi.")
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
        f"📚 **{category} testlari**\n\nJami: {len(tests)} ta test.",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.callback_query(F.data.startswith("test_"))
async def send_test(callback: types.CallbackQuery):
    data = callback.data.split("_")
    category = data[1]  # ielts yoki sat
    index = int(data[2])

    tests = IELTS_TESTS if category == "ielts" else SAT_TESTS
    if index >= len(tests):
        await callback.answer("❌ Bunday test mavjud emas!", show_alert=True)
        return

    test = tests[index]
    try:
        await callback.message.bot.forward_message(
            chat_id=callback.message.chat.id,
            from_chat_id=test['chat_id'],
            message_id=test['message_id']
        )
        await callback.answer(f"✅ Test {index+1} yuborildi!")
    except Exception as e:
        await callback.answer(f"❌ Xatolik: {e}", show_alert=True)

@router.callback_query(F.data == "back_to_tests")
async def back_to_tests(callback: types.CallbackQuery):
    await callback.message.delete()
    await tests_menu(callback.message, None)
    await callback.answer()

@router.message(F.text == "🔙 Asosiy menyu")
async def back_to_main_tests(message: types.Message, state: FSMContext):
    await state.clear()
    from handlers.start import cmd_start
    await cmd_start(message)

@router.message(F.text == "/get_id")
async def get_message_id(message: types.Message):
    if not message.reply_to_message:
        await message.reply("❌ Iltimos, xabarga reply qiling.")
        return
    chat_id = message.reply_to_message.chat.id
    msg_id = message.reply_to_message.message_id
    await message.reply(
        f"📌 **Xabar ID:**\n"
        f"Chat ID: `{chat_id}`\n"
        f"Message ID: `{msg_id}`",
        parse_mode="Markdown"
    )