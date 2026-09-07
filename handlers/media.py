from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
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

CATEGORY_BUTTON_MAP = {
    BTN_MEDIA_MOVIES: "movies",
    BTN_MEDIA_CARTOONS: "cartoons",
    BTN_MEDIA_ANIME: "anime",
    BTN_MEDIA_MOVIES_EN: "movies",
    BTN_MEDIA_CARTOONS_EN: "cartoons",
    BTN_MEDIA_ANIME_EN: "anime",
}


class MediaStates(StatesGroup):
    choosing_language = State()
    choosing_category = State()


def _source(lang: str) -> dict:
    return UZB_MEDIA if lang == "uz" else ENG_MEDIA


def _total_pages(total: int) -> int:
    return max(1, -(-total // PAGE_SIZE))  # ceil division


# ---------------- Render funksiyalari (matn + inline klaviatura) ----------------


def render_media_list(lang: str, category: str, page: int):
    """Filmlar / Multfilmlar ro'yxati uchun sahifalangan inline klaviatura."""
    items = _source(lang).get(category, [])
    total = len(items)
    start = page * PAGE_SIZE
    end = start + PAGE_SIZE
    page_items = items[start:end]

    kb = InlineKeyboardBuilder()
    for idx, item in enumerate(page_items, start=start):
        kb.button(text=item["title"], callback_data=f"mli:{lang}:{category}:{idx}")
    kb.adjust(1)

    nav_row = []
    if page > 0:
        nav_row.append(("◀️ Oldingi", f"mlp:{lang}:{category}:{page - 1}"))
    if end < total:
        nav_row.append(("Keyingi ▶️", f"mlp:{lang}:{category}:{page + 1}"))
    if nav_row:
        kb.row(*[_btn(t, c) for t, c in nav_row])

    kb.row(_btn("🔙 Orqaga", f"mlb:{lang}"))

    text = f"📋 Ro'yxat ({page + 1}/{_total_pages(total)}):"
    return text, kb.as_markup()


def render_anime_list(lang: str, page: int):
    """Anime nomlari ro'yxati uchun sahifalangan inline klaviatura."""
    animes = _source(lang).get("anime", [])
    total = len(animes)
    start = page * PAGE_SIZE
    end = start + PAGE_SIZE
    page_items = animes[start:end]

    kb = InlineKeyboardBuilder()
    for idx, anime in enumerate(page_items, start=start):
        kb.button(text=anime["title"], callback_data=f"ali:{lang}:{idx}")
    kb.adjust(1)

    nav_row = []
    if page > 0:
        nav_row.append(("◀️ Oldingi", f"alp:{lang}:{page - 1}"))
    if end < total:
        nav_row.append(("Keyingi ▶️", f"alp:{lang}:{page + 1}"))
    if nav_row:
        kb.row(*[_btn(t, c) for t, c in nav_row])

    kb.row(_btn("🔙 Orqaga", f"alb:{lang}"))

    text = f"🀄 Animeni tanlang ({page + 1}/{_total_pages(total)}):"
    return text, kb.as_markup()


def render_episode_list(lang: str, anime_idx: int, page: int):
    """Tanlangan animening qismlari (1, 2, 3, ...) uchun sahifalangan inline klaviatura."""
    animes = _source(lang).get("anime", [])
    anime = animes[anime_idx]
    episodes = anime.get("episodes", [])
    total = len(episodes)
    start = page * PAGE_SIZE
    end = start + PAGE_SIZE
    page_items = episodes[start:end]

    kb = InlineKeyboardBuilder()
    for idx, ep in enumerate(page_items, start=start):
        label = ep.get("title") or f"{idx + 1}-qism"
        kb.button(text=label, callback_data=f"eli:{lang}:{anime_idx}:{idx}")
    kb.adjust(1)

    nav_row = []
    if page > 0:
        nav_row.append(("◀️ Oldingi", f"elp:{lang}:{anime_idx}:{page - 1}"))
    if end < total:
        nav_row.append(("Keyingi ▶️", f"elp:{lang}:{anime_idx}:{page + 1}"))
    if nav_row:
        kb.row(*[_btn(t, c) for t, c in nav_row])

    kb.row(_btn("🔙 Orqaga", f"elb:{lang}"))

    text = f"🎬 {anime['title']} — qismlar ({page + 1}/{_total_pages(total)}):"
    return text, kb.as_markup()


def _btn(text: str, callback_data: str):
    from aiogram.types import InlineKeyboardButton

    return InlineKeyboardButton(text=text, callback_data=callback_data)


# ---------------- Reply-klaviatura bosqichlari (til / kategoriya) ----------------


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


@router.message(MediaStates.choosing_category, F.text.in_(CATEGORY_BUTTON_MAP.keys()))
async def choose_media_category(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get("media_lang", "uz")
    category = CATEGORY_BUTTON_MAP[message.text]

    if category == "anime":
        items = _source(lang).get("anime", [])
        if not items:
            await message.answer("😔 Hozircha bu kategoriyada kontent mavjud emas.")
            return
        text, markup = render_anime_list(lang, 0)
    else:
        items = _source(lang).get(category, [])
        if not items:
            await message.answer("😔 Hozircha bu kategoriyada kontent mavjud emas.")
            return
        text, markup = render_media_list(lang, category, 0)

    await message.answer(text, reply_markup=markup)


# ---------------- Inline callback handlerlar: Filmlar / Multfilmlar ----------------


@router.callback_query(F.data.startswith("mlp:"))
async def movie_list_page(callback: CallbackQuery) -> None:
    _, lang, category, page = callback.data.split(":")
    text, markup = render_media_list(lang, category, int(page))
    await callback.message.edit_text(text, reply_markup=markup)
    await callback.answer()


@router.callback_query(F.data.startswith("mli:"))
async def movie_item_selected(callback: CallbackQuery) -> None:
    _, lang, category, idx = callback.data.split(":")
    idx = int(idx)
    items = _source(lang).get(category, [])

    if idx < 0 or idx >= len(items):
        await callback.answer("⚠️ Topilmadi", show_alert=True)
        return

    item = items[idx]
    try:
        await callback.bot.copy_message(
            chat_id=callback.message.chat.id,
            from_chat_id=item["chat_id"],
            message_id=item["message_id"],
        )
        await callback.answer()
    except Exception as e:
        await callback.answer(f"⚠️ Xatolik: {e}", show_alert=True)


@router.callback_query(F.data.startswith("mlb:"))
async def back_from_movie_list(callback: CallbackQuery, state: FSMContext) -> None:
    _, lang = callback.data.split(":")
    await state.set_state(MediaStates.choosing_category)
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer("🎬 Kategoriyani tanlang:", reply_markup=media_category_kb(lang))
    await callback.answer()


# ---------------- Inline callback handlerlar: Anime ro'yxati ----------------


@router.callback_query(F.data.startswith("alp:"))
async def anime_list_page(callback: CallbackQuery) -> None:
    _, lang, page = callback.data.split(":")
    text, markup = render_anime_list(lang, int(page))
    await callback.message.edit_text(text, reply_markup=markup)
    await callback.answer()


@router.callback_query(F.data.startswith("ali:"))
async def anime_item_selected(callback: CallbackQuery) -> None:
    _, lang, anime_idx = callback.data.split(":")
    anime_idx = int(anime_idx)
    animes = _source(lang).get("anime", [])

    if anime_idx < 0 or anime_idx >= len(animes):
        await callback.answer("⚠️ Topilmadi", show_alert=True)
        return

    text, markup = render_episode_list(lang, anime_idx, 0)
    await callback.message.edit_text(text, reply_markup=markup)
    await callback.answer()


@router.callback_query(F.data.startswith("alb:"))
async def back_from_anime_list(callback: CallbackQuery, state: FSMContext) -> None:
    _, lang = callback.data.split(":")
    await state.set_state(MediaStates.choosing_category)
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer("🎬 Kategoriyani tanlang:", reply_markup=media_category_kb(lang))
    await callback.answer()


# ---------------- Inline callback handlerlar: Anime qismlari (episodes) ----------------


@router.callback_query(F.data.startswith("elp:"))
async def episode_list_page(callback: CallbackQuery) -> None:
    _, lang, anime_idx, page = callback.data.split(":")
    text, markup = render_episode_list(lang, int(anime_idx), int(page))
    await callback.message.edit_text(text, reply_markup=markup)
    await callback.answer()


@router.callback_query(F.data.startswith("eli:"))
async def episode_selected(callback: CallbackQuery) -> None:
    _, lang, anime_idx, ep_idx = callback.data.split(":")
    anime_idx = int(anime_idx)
    ep_idx = int(ep_idx)
    animes = _source(lang).get("anime", [])

    if anime_idx < 0 or anime_idx >= len(animes):
        await callback.answer("⚠️ Topilmadi", show_alert=True)
        return

    episodes = animes[anime_idx].get("episodes", [])
    if ep_idx < 0 or ep_idx >= len(episodes):
        await callback.answer("⚠️ Topilmadi", show_alert=True)
        return

    ep = episodes[ep_idx]
    try:
        await callback.bot.copy_message(
            chat_id=callback.message.chat.id,
            from_chat_id=ep["chat_id"],
            message_id=ep["message_id"],
        )
        await callback.answer()
    except Exception as e:
        await callback.answer(f"⚠️ Xatolik: {e}", show_alert=True)


@router.callback_query(F.data.startswith("elb:"))
async def back_from_episode_list(callback: CallbackQuery) -> None:
    _, lang = callback.data.split(":")
    text, markup = render_anime_list(lang, 0)
    await callback.message.edit_text(text, reply_markup=markup)
    await callback.answer()