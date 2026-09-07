# HyMind Telegram Bot

Ma'lumotlar bazasisiz (database-free), ID fayllarga asoslangan Telegram bot.
Aiogram 3.19.0 ustida yozilgan.

## Xususiyatlar

- 🌐 Til tanlash (O'zbek / English) — xotirada saqlanadi, bot restart bo'lsa qayta so'raladi
- 🌍 **Tarjima** — matnni Oʻzbekcha / Ruscha / English tillariga tarjima qilish (`deep-translator`)
- 📝 **Tests** — IELTS / SAT testlari, yopiq guruhdan `copy_message` orqali yuboriladi
- 🎬 **Media** — Filmlar / Multfilmlar / Animelar, til va kategoriya bo'yicha
- 🆘 **Support** — Admin bilan bog'lanish, taklif yozish, qo'llab-quvvatlash (karta raqami)

Hech qanday SQL/NoSQL baza ishlatilmaydi. Barcha kontent (test, media)
yopiq Telegram guruh/kanalda saqlanadi; bot faqat `chat_id` va `message_id`
ni `test_ids.py` / `media_ids.py` fayllaridan o'qib, `copy_message` orqali
foydalanuvchiga uzatadi.

## O'rnatish

1. Repozitoriyani klon qiling va papkaga kiring:
   ```bash
   git clone <repo_url>
   cd hymind_bot
   ```

2. Virtual muhit yarating va kutubxonalarni o'rnating:
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. `.env.dist` faylidan nusxa olib `.env` yarating va tokeningizni kiriting:
   ```bash
   cp .env.dist .env
   ```
   ```
   BOT_TOKEN=123456:ABC-DEF1234...
   ```

4. `config.py` ichida o'z Telegram ID'ingizni `ADMIN_IDS` ga, admin
   username'ingizni `ADMIN_USERNAME` ga va karta raqamingizni
   `SUPPORT_CARD_NUMBER` ga yozing.

5. Botni ishga tushiring:
   ```bash
   python main.py
   ```

## Yopiq guruhdan ID olish

1. Botni yopiq guruh/kanalga admin qilib qo'shing.
2. Guruhga test yoki media faylini joylang.
3. O'sha xabarga **reply** qilib `/get_id` buyrug'ini yuboring (faqat
   `config.py` dagi `ADMIN_IDS` ro'yxatidagilar uchun ishlaydi).
4. Bot sizga `chat_id` va `message_id` ni qaytaradi.
5. Bu qiymatlarni tegishli `title` bilan birga `test_ids.py` yoki
   `media_ids.py` fayliga qo'shing.

## Papkalar tuzilishi

```
hymind_bot/
├── handlers/
│   ├── __init__.py
│   ├── start.py          # /start, til tanlash, asosiy menyu
│   ├── translate.py      # Tarjima bo'limi
│   ├── tests.py          # Tests bo'limi + /get_id
│   ├── media.py          # Media bo'limi
│   ├── support.py        # Support bo'limi
│   └── language_state.py # Tilni xotirada saqlash
├── keyboards/
│   ├── __init__.py
│   └── main.py           # Barcha reply-klaviaturalar
├── .env / .env.dist
├── config.py
├── main.py
├── requirements.txt
├── test_ids.py
├── media_ids.py
└── README.md
```

## Deploy (Railway)

```bash
git add .
git commit -m "Yangilanish"
git push
```

Railway loyihani avtomatik deploy qiladi va `main.py` orqali botni ishga
tushiradi. `BOT_TOKEN` muhit o'zgaruvchisini Railway paneliga qo'shishni
unutmang. Hech qanday ma'lumotlar bazasi sozlamasi kerak emas.

## Eslatmalar

- Til va FSM holatlari xotirada (`MemoryStorage`) saqlanadi — bot qayta
  ishga tushirilganda tozalanadi. Ko'p instansiyali (masalan, bir nechta
  worker) muhitda ishlatmoqchi bo'lsangiz, `RedisStorage` ga o'tishni
  ko'rib chiqing.
- `copy_message` ishlatilgani uchun yuborilgan xabarlarda "Forwarded"
  belgisi chiqmaydi.
