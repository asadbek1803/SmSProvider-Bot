from aiogram import Router, F, types
from aiogram.types import FSInputFile

router = Router()


@router.message(F.text == "📡 SMS providerlarni ko'rish")
async def show_providers(message: types.Message):
    photo = FSInputFile("data/devsms.jpg")
    await message.answer_photo(
        photo=photo,
        caption="📡 <b>Bizning Provider: DevSMS</b>\n\n"
                "💰 Tarif 1 ta SMS: <b>200 SO'M</b> \n"
                "📶 UzMobile, Beeline, Ucell va boshqa operatorlar bilan ishlay oladi"
    )
