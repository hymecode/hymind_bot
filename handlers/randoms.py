from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import random

router = Router()

# Foydalanuvchi sessiyalari (xotirda saqlanadi)
user_sessions = {}

class RandomState(StatesGroup):
    active = State()

@router.message(F.text == "🎲 Randoms")
async def randoms_menu(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    
    # Sessiyani tozalash (yangi kirishda)
    if user_id in user_sessions:
        user_sessions[user_id]['played_songs'] = []
        user_sessions[user_id]['played_words'] = []
    else:
        user_sessions[user_id] = {
            'played_songs': [],
            'played_words': []
        }
    
    await state.set_state(RandomState.active)
    
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="🎵 Random Song")],
            [types.KeyboardButton(text="📝 Random Words")],
            [types.KeyboardButton(text="🔙 Asosiy menyu")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    await message.answer(
        "🎲 **Randoms** bo'limi\n\n"
        "Quyidagi tugmalardan birini tanlang:\n"
        "🎵 - Guruhdagi musiqalardan random 1 tasi\n"
        "📝 - Guruhdagi so'zlardan random 1 tasi\n\n"
        "⚠️ Har safar oldingi tanlanganlardan tashqari random tanlanadi.\n"
        "🔄 Barchasi tanlanganda qayta boshlanadi.\n"
        "🔙 Asosiy menyuga qaytsangiz, ro'yxat tozalanadi.",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.message(RandomState.active, F.text == "🎵 Random Song")
async def random_song(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    CHAT_ID = -1003863295329  # YOPIQ GURUH ID'SI (o'zingiznikiga almashtiring!)
    
    try:
        # Guruhdagi barcha musiqalarni olish
        all_songs = []
        async for msg in message.bot.get_chat_history(CHAT_ID, limit=100):
            if msg.audio or msg.voice or msg.document:
                all_songs.append(msg)
        
        if not all_songs:
            await message.answer("❌ Guruhda hech qanday musiqa topilmadi!")
            return
        
        # Sessiyani tekshirish
        if user_id not in user_sessions:
            user_sessions[user_id] = {'played_songs': [], 'played_words': []}
        
        played = user_sessions[user_id]['played_songs']
        
        # Tanlanmagan musiqalarni topish
        available = [msg for msg in all_songs if msg.message_id not in played]
        
        # Agar barchasi tanlangan bo'lsa
        if not available:
            user_sessions[user_id]['played_songs'] = []
            played = []
            available = all_songs.copy()
            await message.answer(
                "🔄 **Barcha musiqalarni eshitdingiz!**\n"
                "Qayta random boshlanadi...",
                parse_mode="Markdown"
            )
        
        # Random tanlash
        selected = random.choice(available)
        played.append(selected.message_id)
        user_sessions[user_id]['played_songs'] = played
        
        # Yuborish
        if selected.audio:
            await message.answer_audio(
                audio=selected.audio.file_id,
                caption=f"🎵 {selected.caption or 'Navbatdagi qo\'shiq'}\n"
                        f"📊 Eshitilgan: {len(played)}/{len(all_songs)}"
            )
        elif selected.voice:
            await message.answer_voice(
                voice=selected.voice.file_id,
                caption=f"🎵 Ovozli xabar\n📊 Eshitilgan: {len(played)}/{len(all_songs)}"
            )
        elif selected.document:
            await message.answer_document(
                document=selected.document.file_id,
                caption=f"📄 {selected.caption or 'Musiqa fayli'}\n"
                        f"📊 Eshitilgan: {len(played)}/{len(all_songs)}"
            )
        
    except Exception as e:
        await message.answer(f"❌ Xatolik: {e}\nQayta urinib ko'ring.")

@router.message(RandomState.active, F.text == "📝 Random Words")
async def random_words(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    CHAT_ID = -1001234567890  # YOPIQ GURUH ID'SI (o'zingiznikiga almashtiring!)
    
    try:
        # Guruhdagi barcha matnli xabarlarni olish
        all_words = []
        async for msg in message.bot.get_chat_history(CHAT_ID, limit=100):
            if msg.text or msg.caption:
                all_words.append(msg)
        
        if not all_words:
            await message.answer("❌ Guruhda hech qanday so'z topilmadi!")
            return
        
        # Sessiyani tekshirish
        if user_id not in user_sessions:
            user_sessions[user_id] = {'played_songs': [], 'played_words': []}
        
        played = user_sessions[user_id]['played_words']
        
        # Tanlanmagan so'zlarni topish
        available = [msg for msg in all_words if msg.message_id not in played]
        
        # Agar barchasi tanlangan bo'lsa
        if not available:
            user_sessions[user_id]['played_words'] = []
            played = []
            available = all_words.copy()
            await message.answer(
                "🔄 **Barcha so'zlarni ko'rib chiqdingiz!**\n"
                "Qayta random boshlanadi...",
                parse_mode="Markdown"
            )
        
        # Random tanlash
        selected = random.choice(available)
        played.append(selected.message_id)
        user_sessions[user_id]['played_words'] = played
        
        # Yuborish
        content = selected.text or selected.caption or "So'z topilmadi"
        await message.answer(
            f"📝 **Navbatdagi random so'z**\n"
            f"📊 Ko'rilgan: {len(played)}/{len(all_words)}\n\n"
            f"{content}",
            parse_mode="Markdown"
        )
        
    except Exception as e:
        await message.answer(f"❌ Xatolik: {e}\nQayta urinib ko'ring.")

@router.message(RandomState.active, F.text == "🔙 Asosiy menyu")
async def back_to_main_randoms(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    
    # Sessiyani tozalash
    if user_id in user_sessions:
        user_sessions[user_id]['played_songs'] = []
        user_sessions[user_id]['played_words'] = []
    
    await state.clear()
    await message.answer(
        "✅ **Randoms** bo'limidan chiqdingiz.\n"
        "Tanlangan ro'yxat tozalandi.",
        parse_mode="Markdown"
    )
    from handlers.start import cmd_start
    await cmd_start(message)