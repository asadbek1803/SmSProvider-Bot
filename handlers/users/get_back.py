from aiogram import Router, F, types
from keyboards.reply.user import get_user_full_controll_button
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(F.text == "🔙 Qaytish")
async def get_back(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("🏡 Bosh sahifa", reply_markup=get_user_full_controll_button())
