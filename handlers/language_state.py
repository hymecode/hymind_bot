# handlers/language_state.py

# Foydalanuvchi tillarini xotirada saqlash (bot restartda tozalanadi)
user_languages = {}

def set_language(user_id, lang):
    user_languages[user_id] = lang

def get_language(user_id):
    return user_languages.get(user_id, None)