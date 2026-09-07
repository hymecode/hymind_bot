"""
Foydalanuvchi tilini xotirada (RAM) saqlaydigan modul.
Ma'lumotlar bazasi ishlatilmaydi - bot qayta ishga tushirilsa (restart),
bu dict tozalanadi va foydalanuvchidan til qayta so'raladi.
"""

# user_id -> "uz" | "en" | "ru"
user_languages: dict[int, str] = {}


def set_language(user_id: int, lang: str) -> None:
    user_languages[user_id] = lang


def get_language(user_id: int) -> str | None:
    return user_languages.get(user_id)


def has_language(user_id: int) -> bool:
    return user_id in user_languages
