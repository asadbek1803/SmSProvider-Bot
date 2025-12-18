import os
import requests
import openpyxl
from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext
from states.send_sms import SendSMS
from keyboards.reply.user import get_back_button, get_user_full_controll_button
from loader import bot

router = Router()

@router.message(F.text == "💬 SMS yuborish")
async def start_send_sms(message: types.Message, state: FSMContext):
    await state.set_state(SendSMS.file)
    await message.answer("📂 Excel faylni yuboring (.xlsx):\n\n"
                         "📋 <b>Format:</b>\n"
                         "A ustun: ID\n"
                         "B ustun: Ism Familiya\n"
                         "C ustun: Telefon\n"
                         "D ustun: Qarz Miqdori\n"
                         "E ustun: Oxirgi Tashrif",
                         reply_markup=get_back_button())

@router.message(SendSMS.file, F.document)
async def get_sms_file(message: types.Message, state: FSMContext):
    file_id = message.document.file_id
    file_name = message.document.file_name
    
    if not file_name.endswith('.xlsx'):
        await message.answer("❌ Iltimos faqat .xlsx formatdagi excel fayl yuboring.", reply_markup=get_back_button())
        return

    # Download file
    file = await bot.get_file(file_id)
    file_path = file.file_path
    destination = f"data/{file_name}"
    await bot.download_file(file_path, destination)
    
    await message.answer("⏳ Fayl o'qilmoqda va xabarlar yuborilmoqda...")

    # Process Excel
    try:
        wb = openpyxl.load_workbook(destination)
        ws = wb.active
        
        success_count = 0
        fail_count = 0
        
        api_url = "https://devsms.uz/api/send_sms.php"
        headers = {
            "Authorization": f"Bearer {os.getenv('API_TOKEN')}",
            "Content-Type": "application/json"
        }
        
        template_request_sent = False

        # Iterate rows
        # Columns: A=ID(0), B=Name(1), C=Phone(2), D=Amount(3), E=LastVisit(4)
        for row in ws.iter_rows(min_row=2, values_only=True): # Start from row 2 to skip header
            if not row or not row[2]: # Check if Phone exists
                continue
            
            phone = str(row[2])
            phone = phone.replace("+", "").replace(" ", "").replace("-", "")
            
            name = str(row[1]) if len(row) > 1 and row[1] else "Mijoz"
            amount = str(row[3]) if len(row) > 3 and row[3] else "0"
            
            # Construct dynamic message
            sms_text = (f"Dental Clinik: Hurmatli {name}! Bizning shifoxonadan {amount} so'm "
                        f"qarzdorlik aniqlandi. Qarzni o'z vaqtida to'lashingizni so'raymiz.")
            
            payload = {
                "phone": phone,
                "message": sms_text,
                "from": "4546" 
            }
            
            try:
                # Using requests logic
                response = requests.post(api_url, json=payload, headers=headers)
                
                if response.status_code == 200 and response.json().get("success"):
                    success_count += 1
                elif response.status_code == 400:
                    # Auto-add template if moderation error
                    if not template_request_sent:
                        template_url = "https://devsms.uz/user/templates.php" 
                        template_payload = {
                            "name": "Auto Template Debt", 
                            "text": sms_text
                        }
                        try:
                            requests.post(template_url, json=template_payload, headers=headers)
                            await message.answer("⚠️ Ushbu xabar uchun shablon moderatsiyaga yuborildi.")
                        except:
                            pass
                        template_request_sent = True
                    fail_count += 1
                else:
                    fail_count += 1
            except Exception as e:
                print(f"Error sending to {phone}: {e}")
                fail_count += 1
        
        # Remove file after processing
        os.remove(destination)
        
        await message.answer(
            f"✅ Yakunlandi!\n\n"
            f"🟢 Muvaffaqiyatli: {success_count} ta\n"
            f"🔴 Xatolik: {fail_count} ta",
            reply_markup=get_user_full_controll_button()
        )
        await state.clear()
        
    except Exception as e:
        await message.answer(f"❌ Faylni o'qishda xatolik: {e}")
        # cleanup if exists
        if os.path.exists(destination):
            os.remove(destination)
