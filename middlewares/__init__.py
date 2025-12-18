from aiogram import Dispatcher
from .access import AccessMiddleware

def setup(dp: Dispatcher):
    dp.message.middleware(AccessMiddleware())
