from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.main import (
    media_lang_kb,
    media_category_kb,
    main_menu_kb,
    BTN_MEDIA,
    BTN_BACK,
    BTN_LANG_UZ,
    BTN_LANG_EN,
    BTN_MEDIA_MOVIES,
    BTN_MEDIA_CARTOONS,
    BTN_MEDIA_ANIME,
    BTN_MEDIA_MOVIES_EN,
    BTN_MEDIA_CARTOONS_EN,
    BTN_MEDIA_ANIME_EN,
)
from media_ids import UZB_MEDIA, ENG_MEDIA

router = Router(name="media")
PAGE_SIZE = 10

class MediaStates(StatesGroup):
    choosing_language = State()
    choosing_category = State()

def _source(lang: str) -> dict:
    return UZB_MEDIA if lang == "uz" else ENG_MEDIA

def _total_pages(total: int) -> int:
    return max(1, -(-total // PAGE_SIZE))

def _get_items(lang: str, category: str) -> list:
    return _source(lang).get(category, [])


# ----------------- YANGI UNIVERSAL FUNKSIYALAR -----------------

def render_list(lang: str, category: str, page: int):
    """Oddiy va qismli (episodes) elementlarni bitta ro'yxatda ko'rsatadi."""
    items = _get_items(lang, category)
    total = len(items)
    start = page * PAGE_SIZE
    end = start + PAGE_SIZE
    page_items = items[start:end]

    kb = InlineKeyboardBuilder()
    for idx, item in enumerate(page_items, start=start):
        kb.button(text=item["title"], callback_data=f"li:{lang}:{category}:{idx}")
    kb.adjust(1)

    nav_row = []
    if page > 0:
        nav_row.append(("◀️ Oldingi", f"lp:{lang}:{category}:{page - 1}"))
    if end < total:
        nav_row.append(("Keyingi ▶️", f"lp:{lang}:{category}:{page + 1}"))
    if nav_row:
        kb.row(*[InlineKeyboardButton(text=t, callback_data=c) for t, c in nav_row])

    kb.row(InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"lb:{lang}"))
    text = f"📋 Ro'yxat ({page + 1}/{_total_pages(total)}):"
    return text, kb.as_markup()


def render_episodes(lang: str, category: str, item_idx: int, page: int):
    """Tanlangan elementning ichki qismlarini (episodes) ko'rsatadi."""
    items = _get_items(lang, category)
    item = items[item_idx]
    episodes = item.get("episodes", [])
    total = len(episodes)
    start = page * PAGE_SIZE
    end = start + PAGE_SIZE
    page_items = episodes[start:end]

    kb = InlineKeyboardBuilder()
    for ep_idx, ep in enumerate(page_items, start=start):
        label = ep.get("title") or f"{ep_idx + 1}-qism"
        kb.button(text=label, callback_data=f"ei:{lang}:{category}:{item_idx}:{ep_idx}")
    kb.adjust(1)

    nav_row = []
    if page > 0:
        nav_row.append(("◀️ Oldingi", f"ep:{lang}:{category}:{item_idx}:{page - 1}"))
    if end < total:
        nav_row.append(("Keyingi ▶️", f"ep:{lang}:{category}:{item_idx}:{page + 1}"))
    if nav_row:
        kb.row(*[InlineKeyboardButton(text=t, callback_data=c) for t, c in nav_row])

    kb.row(InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"elb:{lang}:{category}:{item_idx}"))
    text = f"🎬 {item['title']} — qismlar ({page + 1}/{_total_pages(total)}):"
    return text, kb.as_markup()


# ----------------- REPLY KLATURASI (FSM) -----------------

@router.message(F.text == BTN_MEDIA)
async def open_media_menu(message: Message, state: FSMContext) -> None:
    await state.set_state(MediaStates.choosing_language)
    await message.answer("🌐 Tilni tanlang:", reply_markup=media_lang_kb())


@router.message(MediaStates.choosing_language, F.text == BTN_BACK)
async def back_from_media_lang(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("🔙 Asosiy menyu", reply_markup=main_menu_kb())


@router.message(MediaStates.choosing_language, F.text.in_({BTN_LANG_UZ, BTN_LANG_EN}))
async def choose_media_language(message: Message, state: FSMContext) -> None:
    lang = "uz" if message.text == BTN_LANG_UZ else "en"
    await state.update_data(media_lang=lang)
    await state.set_state(MediaStates.choosing_category)
    await message.answer("🎬 Kategoriyani tanlang:", reply_markup=media_category_kb(lang))


@router.message(MediaStates.choosing_category, F.text == BTN_BACK)
async def back_from_media_category(message: Message, state: FSMContext) -> None:
    await state.set_state(MediaStates.choosing_language)
    await message.answer("🌐 Tilni tanlang:", reply_markup=media_lang_kb())


@router.message(MediaStates.choosing_category, F.text.in_({BTN_MEDIA_MOVIES, BTN_MEDIA_CARTOONS, BTN_MEDIA_ANIME, BTN_MEDIA_MOVIES_EN, BTN_MEDIA_CARTOONS_EN, BTN_MEDIA_ANIME_EN}))
async def choose_media_category(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get("media_lang", "uz")
    
    # Category ni topish
    button_map = {
        BTN_MEDIA_MOVIES: "movies", BTN_MEDIA_CARTOONS: "cartoons", BTN_MEDIA_ANIME: "anime",
        BTN_MEDIA_MOVIES_EN: "movies", BTN_MEDIA_CARTOONS_EN: "cartoons", BTN_MEDIA_ANIME_EN: "anime"
    }
    category = button_map[message.text]
    
    items = _get_items(lang, category)
    if not items:
        await message.answer("😔 Hozircha bu kategoriyada kontent mavjud emas.")
        return

    text, markup = render_list(lang, category, 0)
    await message.answer(text, reply_markup=markup)


# ----------------- UNIVERSAL CALLBACK HANDLERLAR -----------------

@router.callback_query(F.data.startswith("li:"))
async def item_selected(callback: CallbackQuery):
    _, lang, category, idx = callback.data.split(":")
    idx = int(idx)
    items = _get_items(lang, category)

    if idx < 0 or idx >= len(items):
        await callback.answer("⚠️ Topilmadi", show_alert=True)
        return

    item = items[idx]

    # Agar ichida episodes bo'lsa, qismlar ro'yxatini ochamiz
    if "episodes" in item:
        text, markup = render_episodes(lang, category, idx, 0)
        await callback.message.edit_text(text, reply_markup=markup)
    else:
        # Oddiy film bo'lsa, darhol yuboramiz
        await callback.bot.copy_message(
            chat_id=callback.message.chat.id,
            from_chat_id=item["chat_id"],
            message_id=item["message_id"],
        )
    await callback.answer()


@router.callback_query(F.data.startswith("ei:"))
async def episode_selected(callback: CallbackQuery):
    _, lang, category, idx, ep_idx = callback.data.split(":")
    idx, ep_idx = int(idx), int(ep_idx)
    items = _get_items(lang, category)
    item = items[idx]
    ep = item["episodes"][ep_idx]
    
    await callback.bot.copy_message(
        chat_id=callback.message.chat.id,
        from_chat_id=ep["chat_id"],
        message_id=ep["message_id"],
    )
    await callback.answer()


@router.callback_query(F.data.startswith("lp:"))
async def list_page(callback: CallbackQuery):
    _, lang, category, page = callback.data.split(":")
    text, markup = render_list(lang, category, int(page))
    await callback.message.edit_text(text, reply_markup=markup)
    await callback.answer()


@router.callback_query(F.data.startswith("ep:"))
async def episode_page(callback: CallbackQuery):
    _, lang, category, idx, page = callback.data.split(":")
    text, markup = render_episodes(lang, category, int(idx), int(page))
    await callback.message.edit_text(text, reply_markup=markup)
    await callback.answer()


@router.callback_query(F.data.startswith("elb:"))
async def back_to_list(callback: CallbackQuery):
    _, lang, category, idx = callback.data.split(":")
    # Orqaga ro'yxatga qaytamiz
    text, markup = render_list(lang, category, 0)
    await callback.message.edit_text(text, reply_markup=markup)
    await callback.answer()


@router.callback_query(F.data.startswith("lb:"))
async def back_to_category(callback: CallbackQuery, state: FSMContext):
    _, lang = callback.data.split(":")
    await state.set_state(MediaStates.choosing_category)
    await callback.message.edit_text("🎬 Kategoriyani tanlang:", reply_markup=media_category_kb(lang))
    await callback.answer()