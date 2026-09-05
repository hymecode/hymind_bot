from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_premium_keyboard(is_premium: bool):
    buttons = []
    
    if is_premium:
        buttons.append([KeyboardButton(text="💳 Premium uzaytirish")])
        buttons.append([KeyboardButton(text="📊 Mening premiumim")])
    else:
        buttons.append([KeyboardButton(text="💳 7 kun (7000 so'm)")])
        buttons.append([KeyboardButton(text="💳 1 oy (15000 so'm)")])
        buttons.append([KeyboardButton(text="🎁 Menda promo-kod bor")])
    
    buttons.append([KeyboardButton(text="🔙 Asosiy menyu")])
    
    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=False
    )