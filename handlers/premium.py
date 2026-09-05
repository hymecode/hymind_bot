from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from utils.database import get_user
from utils.premium import is_premium, get_premium_days_left, extend_premium
from keyboards.premium import get_premium_keyboard, get_payment_keyboard
from datetime import datetime
import re

router = Router()

class PaymentState(StatesGroup):
    waiting_payment = State()  # To'lov skrinshotini kutish

@router.message(F.text == "⭐ Premium")
async def premium_menu(message: types.Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    premium_status = is_premium(user_id)
    
    if premium_status:
        days_left = get_premium_days_left(user_id)
        text = (
            f"⭐ **Siz premium obunasiz!**\n\n"
            f"⏳ Qolgan kun: {days_left} kun\n\n"
            f"🔄 Premiumni uzaytirish uchun pastdagi tugmani bosing."
        )
    else:
        text = (
            "⭐ **Premium obuna**\n\n"
            "Premium obuna orqali siz quyidagi imtiyozlarga ega bo'lasiz:\n"
            "✅ Cheksiz tarjima\n"
            "✅ Pomodoro statistikasi\n"
            "✅ Maxsus funksiyalar\n\n"
            "💳 **Narxlar:**\n"
            "• 7 kun – 7000 so'm\n"
            "• 1 oy – 15000 so'm\n\n"
            "⬇️ Pastdagi tugma orqali to'lov qiling."
        )
    
    await message.answer(text, reply_markup=get_premium_keyboard(premium_status), parse_mode="Markdown")

@router.message(F.text == "💳 7 kun (7000 so'm)")
async def buy_7_days(message: types.Message, state: FSMContext):
    await state.update_data(amount="7000", days=7)
    await message.answer(
        "💳 **To'lov qilish**\n\n"
        "Quyidagi kartaga 7000 so'm to'lov qiling:\n"
        "💳 **8600 1234 5678 9012** (Humo/Uzcard)\n\n"
        "To'lov qilgandan so'ng, quyidagilarni yuboring:\n"
        "1️⃣ Skrinshot (to'lov tasdiqnomasi)\n"
        "2️⃣ Tranzaksiya raqami (to'lov ID si)\n\n"
        "Namuna:\n"
        "`Tranzaksiya: 1234567890`\n\n"
        "⚠️ Iltimos, to'lov miqdori va vaqtini aniq ko'rsating.\n"
        "Admin tekshirib, premiumni faollashtiradi.\n\n"
        "❌ Bekor qilish uchun /cancel buyrug'ini bering.",
        parse_mode="Markdown"
    )
    await state.set_state(PaymentState.waiting_payment)

@router.message(F.text == "💳 1 oy (15000 so'm)")
async def buy_1_month(message: types.Message, state: FSMContext):
    await state.update_data(amount="15000", days=30)
    await message.answer(
        "💳 **To'lov qilish**\n\n"
        "Quyidagi kartaga 15000 so'm to'lov qiling:\n"
        "💳 **8600 1234 5678 9012** (Humo/Uzcard)\n\n"
        "To'lov qilgandan so'ng, quyidagilarni yuboring:\n"
        "1️⃣ Skrinshot (to'lov tasdiqnomasi)\n"
        "2️⃣ Tranzaksiya raqami (to'lov ID si)\n\n"
        "Namuna:\n"
        "`Tranzaksiya: 1234567890`\n\n"
        "⚠️ Iltimos, to'lov miqdori va vaqtini aniq ko'rsating.\n"
        "Admin tekshirib, premiumni faollashtiradi.\n\n"
        "❌ Bekor qilish uchun /cancel buyrug'ini bering.",
        parse_mode="Markdown"
    )
    await state.set_state(PaymentState.waiting_payment)

@router.message(PaymentState.waiting_payment, F.text == "/cancel")
async def cancel_payment(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ To'lov jarayoni bekor qilindi. Qaytadan /start bosing.")

@router.message(PaymentState.waiting_payment, F.photo | F.text)
async def receive_payment(message: types.Message, state: FSMContext, bot):
    data = await state.get_data()
    days = data.get("days", 7)
    amount = data.get("amount", "7000")
    
    user_id = message.from_user.id
    username = message.from_user.username or "mavjud emas"
    first_name = message.from_user.first_name
    
    admin_id = 123456789  # O'ZINGIZNING TELEGRAM ID'NGIZNI YOZING!
    
    if message.photo:
        photo = message.photo[-1]
        caption = f"📸 **Yangi to'lov skrinshoti**\n\n"
        caption += f"👤 Foydalanuvchi: {first_name}\n"
        caption += f"📛 Username: @{username}\n"
        caption += f"🆔 ID: {user_id}\n"
        caption += f"💰 Miqdori: {amount} so'm\n"
        caption += f"📅 Kun: {days} kun\n"
        caption += f"📝 Izoh: {message.caption or 'Yo‘q'}\n\n"
        caption += "✅ Tekshirib, premium berish uchun /verify komandasini bering."
        
        await bot.send_photo(admin_id, photo=photo.file_id, caption=caption, parse_mode="Markdown")
        await message.answer("✅ Skrinshot qabul qilindi! Admin tekshirib, premiumni faollashtiradi. Bu biroz vaqt olishi mumkin.")
    
    elif message.text:
        text = f"📝 **Yangi to'lov ma'lumoti**\n\n"
        text += f"👤 Foydalanuvchi: {first_name}\n"
        text += f"📛 Username: @{username}\n"
        text += f"🆔 ID: {user_id}\n"
        text += f"💰 Miqdori: {amount} so'm\n"
        text += f"📅 Kun: {days} kun\n"
        text += f"📄 Ma'lumot: {message.text}\n\n"
        text += "✅ Tekshirib, premium berish uchun /verify komandasini bering."
        
        await bot.send_message(admin_id, text, parse_mode="Markdown")
        await message.answer("✅ Ma'lumot qabul qilindi! Admin tekshirib, premiumni faollashtiradi.")
    
    await state.clear()

# Admin uchun: Premium berish
@router.message(F.text.startswith("/verify"))
async def verify_payment(message: types.Message):
    admin_id = 123456789  # O'ZINGIZNING TELEGRAM ID'NGIZNI YOZING!
    if message.from_user.id != admin_id:
        await message.answer("❌ Bu buyruq faqat admin uchun!")
        return
    
    try:
        parts = message.text.split()
        if len(parts) < 3:
            await message.answer("❌ Ishlatish: /verify <user_id> <days>\nMisol: /verify 123456789 30")
            return
        
        user_id = int(parts[1])
        days = int(parts[2])
        
        extend_premium(user_id, days)
        await message.answer(f"✅ Foydalanuvchi {user_id} ga {days} kun premium berildi!")
        
        try:
            await message.bot.send_message(user_id, f"🎉 Tabriklaymiz! Sizga {days} kun premium berildi. Endi barcha imtiyozlardan foydalanishingiz mumkin!")
        except:
            pass
            
    except Exception as e:
        await message.answer(f"❌ Xatolik: {e}")