from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.main import (
    tests_menu_kb,
    tests_list_kb,
    main_menu_kb,
    BTN_TESTS,
    BTN_BACK,
    BTN_TEST_IELTS,
    BTN_TEST_SAT,
)
from test_ids import IELTS_TESTS, SAT_TESTS
from config import ADMIN_IDS

router = Router(name="tests")


class TestsStates(StatesGroup):
    choosing_category = State()
    choosing_test = State()


@router.message(F.text == BTN_TESTS)
async def open_tests_menu(message: Message, state: FSMContext) -> None:
    await state.set_state(TestsStates.choosing_category)
    await message.answer("📚 Bo'limni tanlang:", reply_markup=tests_menu_kb())


@router.message(TestsStates.choosing_category, F.text == BTN_BACK)
async def back_from_categories(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("🔙 Asosiy menyu", reply_markup=main_menu_kb())


@router.message(TestsStates.choosing_category, F.text.in_({BTN_TEST_IELTS, BTN_TEST_SAT}))
async def choose_category(message: Message, state: FSMContext) -> None:
    category = "ielts" if message.text == BTN_TEST_IELTS else "sat"
    tests_list = IELTS_TESTS if category == "ielts" else SAT_TESTS

    if not tests_list:
        await message.answer("😔 Hozircha bu bo'limda testlar mavjud emas.")
        return

    titles = [t["title"] for t in tests_list]
    await state.update_data(category=category)
    await state.set_state(TestsStates.choosing_test)
    await message.answer("📄 Testni tanlang:", reply_markup=tests_list_kb(titles))


@router.message(TestsStates.choosing_test, F.text == BTN_BACK)
async def back_from_test_list(message: Message, state: FSMContext) -> None:
    await state.set_state(TestsStates.choosing_category)
    await message.answer("📚 Bo'limni tanlang:", reply_markup=tests_menu_kb())


@router.message(TestsStates.choosing_test, F.text)
async def send_selected_test(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    category = data.get("category")
    tests_list = IELTS_TESTS if category == "ielts" else SAT_TESTS

    selected = next((t for t in tests_list if t["title"] == message.text), None)
    if not selected:
        await message.answer("⚠️ Bunday test topilmadi, ro'yxatdan tanlang.")
        return

    try:
        await message.bot.copy_message(
            chat_id=message.chat.id,
            from_chat_id=selected["chat_id"],
            message_id=selected["message_id"],
        )
    except Exception as e:
        await message.answer(f"⚠️ Testni yuborishda xatolik: {e}")


# ---------------- Admin: yopiq guruhdan ID olish ----------------


@router.message(Command("get_id"))
async def get_id_command(message: Message) -> None:
    if message.from_user.id not in ADMIN_IDS:
        return  # oddiy foydalanuvchilarga jim javob

    if not message.reply_to_message:
        await message.answer(
            "ℹ️ Bu buyruqni yopiq guruhdagi biror xabarga *reply* qilib yuboring.",
            parse_mode="Markdown",
        )
        return

    replied = message.reply_to_message
    await message.answer(
        f"chat_id: `{replied.chat.id}`\nmessage_id: `{replied.message_id}`",
        parse_mode="Markdown",
    )
