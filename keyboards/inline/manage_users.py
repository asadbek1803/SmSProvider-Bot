from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_users_list_keyboard(users: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    # limits list to recent 20 for simplicity in this turn, ideally pagination
    for user in users:
        # user structure: (id, telegram_id, full_name, is_access)
        user_id = user[0]
        telegram_id = user[1]
        full_name = user[2]
        is_access = user[3]
        
        status_icon = "✅" if is_access else "❌"
        # button text: Name (Status)
        text = f"{status_icon} {full_name}"
        callback_data = f"user_{telegram_id}"
        
        builder.button(text=text, callback_data=callback_data)
        
    builder.adjust(1)
    return builder.as_markup()

def get_user_actions_keyboard(telegram_id: int, is_access: bool) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    toggle_text = "🔒 Bloklash" if is_access else "🔓 Ruxsat berish"
    toggle_callback = f"toggle_{telegram_id}"
    
    delete_text = "🗑 O'chirish"
    delete_callback = f"del_{telegram_id}"
    
    back_text = "🔙 Ro'yxatga qaytish"
    back_callback = "back_to_users"

    builder.button(text=toggle_text, callback_data=toggle_callback)
    builder.button(text=delete_text, callback_data=delete_callback)
    builder.button(text=back_text, callback_data=back_callback)
    
    builder.adjust(1)
    return builder.as_markup()
