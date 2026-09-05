from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import ADMIN_USERNAME, DONATE_CARD, OFFERS_CHAT_ID

router = Router()

class OfferState(StatesGroup):
    waiting_offer = State()

@router.message(F.text == "🆘 Support")
async def support_menu(message: types.Message, state: FSMContext):
    await state.clear()
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="👤 Admin")],
            [types.KeyboardButton(text="💡 Offers")],
            [types.KeyboardButton(text="💰 Support with money")],
            [types.KeyboardButton(text="🔙 Asosiy menyu")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    await message.answer(
        "🆘 **Support** bo'limi\n\n"
        "Quyidagi tugmalardan birini tanlang:\n"
        "👤 - Admin bilan bog'lanish\n"
        "💡 - Taklif yozish\n"
        "💰 - Ijodimni qo'llab-quvvatlash",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.message(F.text == "👤 Admin")
async def admin_contact(message: types.Message):
    await message.answer(
        f"👤 **Admin bilan bog'lanish**\n\n"
        f"Admin: @{ADMIN_USERNAME}\n\n"
        f"📩 Savol yoki muammo bo'lsa, admin bilan bog'lanishingiz mumkin.",
        parse_mode="Markdown"
    )

@router.message(F.text == "💡 Offers")
async def offer_start(message: types.Message, state: FSMContext):
    await state.set_state(OfferState.waiting_offer)
    await message.answer(
        "💡 **Taklif yozish**\n\n"
        "Botni yaxshilash bo'yicha taklifingizni yozib qoldiring.\n"
        "Admin ko'rib chiqadi.\n\n"
        "✍️ Taklif matnini yuboring:\n"
        "❌ Bekor qilish uchun /cancel buyrug'ini bering.",
        parse_mode="Markdown"
    )

@router.message(OfferState.waiting_offer, F.text == "/cancel")
async def cancel_offer(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Taklif yozish bekor qilindi.")

@router.message(OfferState.waiting_offer, F.text)
async def save_offer(message: types.Message, state: FSMContext, bot):
    user_id = message.from_user.id
    username = message.from_user.username or "mavjud emas"
    first_name = message.from_user.first_name
    offer_text = message.text
    
    # Taklifni yopiq guruhga yuborish
    try:
        await bot.send_message(
            chat_id=OFFERS_CHAT_ID,
            text=f"💡 **Yangi taklif**\n\n"
                 f"👤 Foydalanuvchi: {first_name}\n"
                 f"📛 Username: @{username}\n"
                 f"🆔 ID: {user_id}\n\n"
                 f"📝 Taklif:\n{offer_text}",
            parse_mode="Markdown"
        )
        await message.answer("✅ Taklifingiz qabul qilindi! Admin ko'rib chiqadi.")
    except Exception as e:
        await message.answer(f"❌ Xatolik yuz berdi: {e}")
    
    await state.clear()

@router.message(F.text == "💰 Support with money")
async def support_money(message: types.Message):
    await message.answer(
        f"💰 **Ixtiyoriy qo'llab-quvvatlash**\n\n"
        f"Agar bot sizga foydali bo'lsa va ijodimni qo'llab-quvvatlamoqchi bo'lsangiz:\n\n"
        f"💳 **Karta raqami:**\n`{DONATE_CARD}`\n\n"
        f"🙏 Har qanday yordam katta minnatdorchilik bilan qabul qilinadi!",
        parse_mode="Markdown"
    )

@router.message(F.text == "🔙 Asosiy menyu")
async def back_to_main_support(message: types.Message, state: FSMContext):
    await state.clear()
    from handlers.start import cmd_start
    await cmd_start(message)