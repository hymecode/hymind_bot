from aiogram import Router, F, Bot
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.main import (
    support_menu_kb,
    remove_keyboard,
    main_menu_kb,
    BTN_SUPPORT,
    BTN_BACK,
    BTN_SUPPORT_ADMIN,
    BTN_SUPPORT_SUGGEST,
    BTN_SUPPORT_DONATE,
)
from config import ADMIN_IDS, ADMIN_USERNAME, SUPPORT_CARD_NUMBER

router = Router(name="support")


class SupportStates(StatesGroup):
    menu = State()
    waiting_for_suggestion = State()


@router.message(F.text == BTN_SUPPORT)
async def open_support_menu(message: Message, state: FSMContext) -> None:
    await state.set_state(SupportStates.menu)
    await message.answer("🆘 Kerakli bo'limni tanlang:", reply_markup=support_menu_kb())


@router.message(SupportStates.menu, F.text == BTN_BACK)
async def back_from_support_menu(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("🔙 Asosiy menyu", reply_markup=main_menu_kb())


@router.message(SupportStates.menu, F.text == BTN_SUPPORT_ADMIN)
async def show_admin(message: Message) -> None:
    await message.answer(f"👤 Admin bilan bog'lanish uchun: {ADMIN_USERNAME}")


@router.message(SupportStates.menu, F.text == BTN_SUPPORT_DONATE)
async def show_donate_card(message: Message) -> None:
    await message.answer(
        f"💳 Botni qo'llab-quvvatlash uchun karta raqami:\n\n`{SUPPORT_CARD_NUMBER}`",
        parse_mode="Markdown",
    )


@router.message(SupportStates.menu, F.text == BTN_SUPPORT_SUGGEST)
async def ask_for_suggestion(message: Message, state: FSMContext) -> None:
    await state.set_state(SupportStates.waiting_for_suggestion)
    await message.answer(
        "✍️ Taklif yoki fikringizni yozib qoldiring:",
        reply_markup=remove_keyboard(),
    )


@router.message(SupportStates.waiting_for_suggestion, F.text == BTN_BACK)
async def back_from_suggestion(message: Message, state: FSMContext) -> None:
    await state.set_state(SupportStates.menu)
    await message.answer("🆘 Kerakli bo'limni tanlang:", reply_markup=support_menu_kb())


@router.message(SupportStates.waiting_for_suggestion, F.text)
async def receive_suggestion(message: Message, state: FSMContext, bot: Bot) -> None:
    user = message.from_user
    text_for_admins = (
        f"📩 Yangi taklif!\n\n"
        f"👤 Foydalanuvchi: {user.full_name} (@{user.username or 'no_username'})\n"
        f"🆔 ID: {user.id}\n\n"
        f"💬 Matn:\n{message.text}"
    )

    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(chat_id=admin_id, text=text_for_admins)
        except Exception:
            # Admin botni bloklagan yoki chat topilmagan bo'lishi mumkin - o'tkazib yuboramiz
            pass

    await state.set_state(SupportStates.menu)
    await message.answer(
        "✅ Rahmat! Taklifingiz adminlarga yuborildi.",
        reply_markup=support_menu_kb(),
    )
