from aiogram import Router
from . import start, get_balance, add_user, get_back, providers, send_sms, manage_users

router = Router()
router.include_router(get_back.router)
router.include_router(start.router)
router.include_router(get_balance.router)
router.include_router(add_user.router)
router.include_router(providers.router)
router.include_router(send_sms.router)
router.include_router(manage_users.router)

