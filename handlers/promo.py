from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from utils.database import get_db
from utils.premium import extend_premium
from datetime import datetime, timedelta
import random
import string

router = Router()

class PromoState(StatesGroup):
    waiting_code = State()

@router.message(F.text == "🎁 Promo-kod")
async def promo_menu(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "🎁 **Promo-kod bo'limi**\n\n"
        "Agar sizda promo-kod bo'lsa, uni quyidagi formatda yuboring:\n"
        "`KOD: 12345678`\n\n"
        "⚠️ Promo-kod 8 xonali raqamdan iborat.\n"
        "✅ Faqat bir marta ishlatish mumkin.\n\n"
        "❌ Bekor qilish uchun /cancel buyrug'ini bering.",
        parse_mode="Markdown"
    )
    await state.set_state(PromoState.waiting_code)

@router.message(PromoState.waiting_code, F.text == "/cancel")
async def cancel_promo(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Promo-kod tekshiruvi bekor qilindi.")

@router.message(PromoState.waiting_code, F.text)
async def check_promo(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text.strip()
    
    # KOD: 12345678 formatini tekshirish
    if not text.upper().startswith("KOD:"):
        await message.answer("❌ Noto'g'ri format! Iltimos, quyidagi formatda yuboring:\n`KOD: 12345678`")
        return
    
    # KOD: qismini olib tashlash
    code = text[4:].strip()
    
    # 8 xonali raqam ekanligini tekshirish
    if not code.isdigit() or len(code) != 8:
        await message.answer("❌ Promo-kod 8 xonali raqamdan iborat bo'lishi kerak!\nMisol: `KOD: 12345678`")
        return
    
    # Bazadan tekshirish
    conn = get_db()
    promo = conn.execute(
        "SELECT * FROM promo_codes WHERE code = ? AND used_count < max_uses",
        (code,)
    ).fetchone()
    
    if not promo:
        conn.close()
        await message.answer("❌ Promo-kod topilmadi yoki allaqachon ishlatilgan!")
        return
    
    # Foydalanuvchi bu kodni oldin ishlatganmi?
    used = conn.execute(
        "SELECT * FROM promo_usage WHERE user_id = ? AND code = ?",
        (user_id, code)
    ).fetchone()
    
    if used:
        conn.close()
        await message.answer("❌ Siz bu promo-kodni allaqachon ishlatgansiz!")
        return
    
    # Promo-kodni ishlatish
    days = promo["bonus_days"]
    
    # Premium vaqtini uzaytirish
    extend_premium(user_id, days)
    
    # Promo-kod ishlatilganligini qayd qilish
    conn.execute(
        "UPDATE promo_codes SET used_count = used_count + 1 WHERE code = ?",
        (code,)
    )
    conn.execute(
        "INSERT INTO promo_usage (user_id, code) VALUES (?, ?)",
        (user_id, code)
    )
    conn.commit()
    conn.close()
    
    await message.answer(
        f"✅ **Promo-kod qabul qilindi!** 🎉\n\n"
        f"Tabriklaymiz! Sizga {days} kun premium berildi.\n"
        f"Endi barcha premium imtiyozlardan foydalanishingiz mumkin!",
        parse_mode="Markdown"
    )
    await state.clear()

# Admin uchun: Promo-kod yaratish
@router.message(F.text.startswith("/create_promo"))
async def create_promo(message: types.Message):
    admin_id = 123456789  # O'ZINGIZNING TELEGRAM ID'NGIZNI YOZING!
    if message.from_user.id != admin_id:
        await message.answer("❌ Bu buyruq faqat admin uchun!")
        return
    
    try:
        parts = message.text.split()
        if len(parts) < 2:
            await message.answer("❌ Ishlatish: /create_promo <days>\nMisol: /create_promo 30")
            return
        
        days = int(parts[1])
        
        # 8 xonali raqamli kod yaratish
        code = ''.join(random.choices(string.digits, k=8))
        
        conn = get_db()
        conn.execute(
            "INSERT INTO promo_codes (code, bonus_days, max_uses, expires_at) VALUES (?, ?, ?, ?)",
            (code, days, 1, (datetime.now() + timedelta(days=30)).isoformat())
        )
        conn.commit()
        conn.close()
        
        await message.answer(
            f"✅ **Promo-kod yaratildi!**\n\n"
            f"📝 Kod: `{code}`\n"
            f"📅 Kun: {days} kun\n"
            f"📆 Amal qilish muddati: 30 kun\n\n"
            f"Buni do'stingizga bering!",
            parse_mode="Markdown"
        )
        
    except Exception as e:
        await message.answer(f"❌ Xatolik: {e}")