from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from keyboards.inline.access_status import get_access_status_keyboard
from states.add_user import AddUser
from loader import db
from keyboards.reply.user import get_user_full_controll_button, get_back_button

router = Router()

@router.message(F.text == "➕ Foydalanuvchi qo'shish")
async def add_user(message: types.Message, state: FSMContext):
    await state.set_state(AddUser.telegram_id)
    await message.answer("🆔 Foydalanuvchini qo'shish uchun telegram IDni kiriting", reply_markup=get_back_button())

@router.message(AddUser.telegram_id)
async def add_user_id(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
         await message.answer("❌ ID raqam bo'lishi kerak!", reply_markup=get_back_button())
         return

    await state.update_data(telegram_id=int(message.text))
    await state.set_state(AddUser.full_name)
    await message.answer("👤 Foydalanuvchini qo'shish uchun ismini kiriting: ", reply_markup=get_back_button())

@router.message(AddUser.full_name)
async def add_user_full_name(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await state.set_state(AddUser.is_access)
    await message.answer("Foydalanuvchi STATUS (Botga kirishga / Kira olmaydi)", reply_markup=get_access_status_keyboard())

@router.callback_query(AddUser.is_access)
async def add_user_is_access(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    telegram_id = data.get("telegram_id")
    full_name = data.get("full_name")
    
    is_access = callback.data == "access_granted"
    
    # 1. Add user if not exists
    await db.add_user(telegram_id=telegram_id, full_name=full_name)
    # 2. Update status
    await db.update_user_access(telegram_id=telegram_id, is_access=is_access)
    
    status_text = "✅ Aktiv" if is_access else "❌ Bloklangan"
    
    await callback.message.delete()
    await callback.message.answer(f"✅ Foydalanuvchi muvaffaqiyatli saqlandi!\n\n🆔 ID: {telegram_id}\n👤 Ism: {full_name}\n📊 Status: {status_text}")
    await state.clear()
