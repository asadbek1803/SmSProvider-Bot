from aiogram.types import ReplyKeyboardMarkup, KeyboardButton   


def get_back_button() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🔙 Qaytish")
            ]
        ],
        resize_keyboard=True
    )
    

def get_user_full_controll_button() -> ReplyKeyboardMarkup:
    keyboard = [
        [
            KeyboardButton(text="💬 SMS yuborish"),
        ],
        [
            KeyboardButton(text="💰 Balansni ko'rish"),
            KeyboardButton(text="➕ Foydalanuvchi qo'shish")
        ],
        [
            KeyboardButton(text="📡 SMS providerlarni ko'rish"),
            KeyboardButton(text="👥 Foydalanuvchilar")
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
