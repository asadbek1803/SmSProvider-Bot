import os
import requests
from aiogram import Router, F, types
from dotenv import load_dotenv

load_dotenv()
router = Router()

@router.message(F.text == "💰 Balansni ko'rish")
async def get_balance(message: types.Message):
    user = message.from_user
    if not user:
        return
    waiter_msg = await message.answer(text = "⏳ So'rov yuborilmoqda. Iltimos kuting ...") 
    api_url = "https://devsms.uz/api/get_balance.php"
    headers = {
        "Authorization": f"Bearer {os.getenv('API_TOKEN')}",
        "Content-Type": "application/json"
    }
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        data = response.json().get("data", {})
        balance = data.get("balance")
        calculate_sms = int(float(balance)) / 200 
        await waiter_msg.delete()
        await message.answer(f"🪙 Sizning balansingiz: {int(float(balance))} so'm\n💬SMS taqriban: {int(calculate_sms)} ta")
    else:
        await message.answer("Balansni olishda xatolik yuz berish kutilmoqda")


