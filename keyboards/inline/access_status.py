from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def get_access_status_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Aktiv", callback_data="access_granted")
    builder.button(text="❌ Bloklangan", callback_data="access_denied")
    builder.adjust(1) 
    return builder.as_markup()