from aiogram.fsm.state import State, StatesGroup

class SendSMS(StatesGroup):
    file = State()
