from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import ADMIN_IDS

router = Router()

class SupportState(StatesGroup):
    waiting_offer = State()

@router.message(F.text == "🆘 Support")
async def support_menu(message: types.Message, state: FSMContext):
    await state.clear()
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="👤 Admin")],
            [types.KeyboardButton(text="💡 Taklif yozish")],
            [types.KeyboardButton(text="💰 Qo'llab-quvvatlash")],
            [types.KeyboardButton(text="🔙 Asosiy menyu")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    await message.answer(
        "🆘 **Support bo'limi**\n\n"
        "Quyidagi tugmalardan birini tanlang:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.message(F.text == "👤 Admin")
async def contact_admin(message: types.Message):
    admin_username = "HyMe"  # O'zingizning username'ingiz ( @ belgisiz )
    await message.answer(
        f"👤 **Admin:** @{admin_username}\n\n"
        "Savol yoki muammo bo'lsa, admin bilan bog'lanishingiz mumkin.",
        parse_mode="Markdown"
    )

@router.message(F.text == "💡 Taklif yozish")
async def offer_write(message: types.Message, state: FSMContext):
    await state.set_state(SupportState.waiting_offer)
    await message.answer(
        "💡 **Taklif yozish**\n\n"
        "Taklifingizni yozib qoldiring. Admin ko'rib chiqadi.\n"
        "❌ Bekor qilish uchun /cancel buyrug'ini bering.",
        parse_mode="Markdown"
    )

@router.message(SupportState.waiting_offer, F.text)
async def save_offer(message: types.Message, state: FSMContext):
    user = message.from_user
    offer_text = message.text

    # Taklifni adminlarga yuborish
    for admin_id in ADMIN_IDS:
        try:
            await message.bot.send_message(
                admin_id,
                f"💡 **Yangi taklif!**\n\n"
                f"👤 Foydalanuvchi: {user.first_name} (@{user.username or 'mavjud emas'})\n"
                f"🆔 ID: {user.id}\n"
                f"📝 Taklif:\n{offer_text}",
                parse_mode="Markdown"
            )
        except:
            pass

    await message.answer("✅ Taklifingiz qabul qilindi! Rahmat.")
    await state.clear()

@router.message(SupportState.waiting_offer, F.text == "/cancel")
async def cancel_offer(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Taklif yozish bekor qilindi.")

@router.message(F.text == "💰 Qo'llab-quvvatlash")
async def support_with_money(message: types.Message):
    card_number = "8600 1234 5678 9012"  # O'zingizning karta raqamingiz
    await message.answer(
        f"💰 **Loyihani qo'llab-quvvatlash**\n\n"
        f"Agar loyihani qo'llab-quvvatlamoqchi bo'lsangiz, quyidagi kartaga pul o'tkazishingiz mumkin:\n\n"
        f"💳 **{card_number}** (Humo/Uzcard)\n\n"
        f"Rahmat! Sizning yordamingiz loyihani rivojlantirishga yordam beradi.",
        parse_mode="Markdown"
    )

@router.message(F.text == "🔙 Asosiy menyu")
async def back_to_main_support(message: types.Message, state: FSMContext):
    await state.clear()
    from handlers.start import cmd_start
    await cmd_start(message)