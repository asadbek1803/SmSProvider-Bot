from aiogram import Router
from . import users

router = Router()
router.include_router(users.router)
