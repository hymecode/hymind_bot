from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from utils.database import get_db
import random

router = Router()

# Foydalanuvchi sessiyalari (xotirda saqlanadi)
user_sessions = {}

class RandomState(StatesGroup):
    active = State()

@router.message(F.text == "🎲 Randoms")
async def randoms_menu(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    
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
        "🎵 - Bazadagi musiqalardan random 1 tasi\n"
        "📝 - Bazadagi so'zlardan random 1 tasi\n\n"
        "⚠️ Har safar oldingi tanlanganlardan tashqari random tanlanadi.\n"
        "🔄 Barchasi tanlanganda qayta boshlanadi.\n"
        "🔙 Asosiy menyuga qaysangiz, ro'yxat tozalanadi.",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.message(RandomState.active, F.text == "🎵 Random Song")
async def random_song(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    
    # Bazadan barcha musiqalarni olish
    conn = get_db()
    all_songs = conn.execute("SELECT * FROM songs ORDER BY id").fetchall()
    conn.close()
    
    if not all_songs:
        await message.answer("❌ Bazada hech qanday musiqa yo'q!\nAdmin musiqa qo'shsin.")
        return
    
    if user_id not in user_sessions:
        user_sessions[user_id] = {'played_songs': [], 'played_words': []}
    
    played = user_sessions[user_id]['played_songs']
    
    # Tanlanmaganlarni topish (id bo'yicha)
    available = [song for song in all_songs if song['id'] not in played]
    
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
    played.append(selected['id'])
    user_sessions[user_id]['played_songs'] = played
    
    # Yopiq guruhdan xabarni forward qilish
    try:
        await message.bot.forward_message(
            chat_id=message.chat.id,
            from_chat_id=selected['chat_id'],
            message_id=selected['message_id']
        )
        # Statistikani yuborish (ixtiyoriy)
        await message.answer(
            f"📊 Eshitilgan: {len(played)}/{len(all_songs)}",
            reply_to_message_id=message.message_id
        )
    except Exception as e:
        await message.answer(f"❌ Xatolik: {e}\n\nQayta urinib ko'ring.")

@router.message(RandomState.active, F.text == "📝 Random Words")
async def random_words(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    
    # Bazadan barcha so'zlarni olish
    conn = get_db()
    all_words = conn.execute("SELECT * FROM words ORDER BY id").fetchall()
    conn.close()
    
    if not all_words:
        await message.answer("❌ Bazada hech qanday so'z yo'q!\nAdmin so'z qo'shsin.")
        return
    
    if user_id not in user_sessions:
        user_sessions[user_id] = {'played_songs': [], 'played_words': []}
    
    played = user_sessions[user_id]['played_words']
    
    available = [word for word in all_words if word['id'] not in played]
    
    if not available:
        user_sessions[user_id]['played_words'] = []
        played = []
        available = all_words.copy()
        await message.answer(
            "🔄 **Barcha so'zlarni ko'rib chiqdingiz!**\n"
            "Qayta random boshlanadi...",
            parse_mode="Markdown"
        )
    
    selected = random.choice(available)
    played.append(selected['id'])
    user_sessions[user_id]['played_words'] = played
    
    # Matnni yuborish
    await message.answer(
        f"📝 **Navbatdagi random so'z**\n"
        f"📊 Ko'rilgan: {len(played)}/{len(all_words)}\n\n"
        f"{selected['content']}",
        parse_mode="Markdown"
    )

@router.message(RandomState.active, F.text == "🔙 Asosiy menyu")
async def back_to_main_randoms(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    
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