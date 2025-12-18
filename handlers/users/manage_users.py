from aiogram import Router, F, types
from loader import db
from keyboards.inline.manage_users import get_users_list_keyboard, get_user_actions_keyboard
from data.config import ADMINS

router = Router()

@router.message(F.text == "👥 Foydalanuvchilar")
async def show_users_list(message: types.Message):
    user = message.from_user
    if user.id not in ADMINS:
        await message.answer("🚫 Bu menyu faqat adminlar uchun!")
        return

    users = await db.select_all_users()
    if not users:
        await message.answer("Foydalanuvchilar topilmadi.")
        return
        
    await message.answer("👥 Foydalanuvchilar ro'yxati:", reply_markup=get_users_list_keyboard(users))

# Callback handler for showing user details
@router.callback_query(F.data.startswith("user_"))
async def show_user_detail(call: types.CallbackQuery):
    telegram_id = int(call.data.split("_")[1])
    user = await db.select_user(telegram_id=telegram_id)
    
    if not user:
        await call.answer("Foydalanuvchi topilmadi", show_alert=True)
        return

    # user: (id, telegram_id, full_name, is_access)
    full_name = user[2]
    is_access = user[3]
    
    status_text = "✅ Aktiv (Ruxsat bor)" if is_access else "❌ Bloklangan (Ruxsat yo'q)"
    
    text = (f"👤 <b>Foydalanuvchi ma'lumotlari:</b>\n\n"
            f"🆔 ID: <code>{telegram_id}</code>\n"
            f"👤 Ism: {full_name}\n"
            f"📊 Status: {status_text}")
            
    await call.message.edit_text(text, reply_markup=get_user_actions_keyboard(telegram_id, is_access))

# Callback for toggling status
@router.callback_query(F.data.startswith("toggle_"))
async def toggle_user_status(call: types.CallbackQuery):
    telegram_id = int(call.data.split("_")[1])
    user = await db.select_user(telegram_id=telegram_id)
    
    if not user:
        await call.answer("Foydalanuvchi topilmadi", show_alert=True)
        return

    current_access = user[3]
    new_access = not current_access
    
    await db.update_user_access(telegram_id=telegram_id, is_access=new_access)
    
    # Reload details
    # We can recursion or copy paste logic. Recursion via calling show_user_detail might need modification of call.data. 
    # Better to just update UI here or simulate user_* call.
    
    # Update UI directly
    user = await db.select_user(telegram_id=telegram_id) # reload
    full_name = user[2]
    is_access = user[3]
    status_text = "✅ Aktiv (Ruxsat bor)" if is_access else "❌ Bloklangan (Ruxsat yo'q)"
    
    text = (f"👤 <b>Foydalanuvchi ma'lumotlari:</b>\n\n"
            f"🆔 ID: <code>{telegram_id}</code>\n"
            f"👤 Ism: {full_name}\n"
            f"📊 Status: {status_text}")
    
    await call.message.edit_text(text, reply_markup=get_user_actions_keyboard(telegram_id, is_access))
    await call.answer(f"Status o'zgartirildi: {status_text}")

# Callback for deleting user
@router.callback_query(F.data.startswith("del_"))
async def delete_user(call: types.CallbackQuery):
    telegram_id = int(call.data.split("_")[1])
    
    await db.delete_user(telegram_id=telegram_id)
    await call.answer("Foydalanuvchi o'chirildi", show_alert=True)
    
    # Return to list
    users = await db.select_all_users()
    if not users:
         await call.message.edit_text("Foydalanuvchilar qolmadi.")
    else:
         await call.message.edit_text("👥 Foydalanuvchilar ro'yxati:", reply_markup=get_users_list_keyboard(users))

# Back button
@router.callback_query(F.data == "back_to_users")
async def back_to_list(call: types.CallbackQuery):
    users = await db.select_all_users()
    await call.message.edit_text("👥 Foydalanuvchilar ro'yxati:", reply_markup=get_users_list_keyboard(users))
