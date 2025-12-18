from aiogram import Router, types
from aiogram.filters import CommandStart
from loader import db
from keyboards.reply.user import get_user_full_controll_button

router = Router()

@router.message(CommandStart())
async def bot_start(message: types.Message):
    user = message.from_user
    if not user:
        return 

    # Add user to database if not exists
    await db.add_user(telegram_id=user.id, full_name=user.full_name)

    await message.answer(
        f"Salom, {message.from_user.full_name}! Siz botdan foydalanishingiz mumkin.",
        reply_markup=get_user_full_controll_button()
    )
