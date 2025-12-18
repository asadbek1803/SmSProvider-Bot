import asyncio
import logging
import sys

from aiogram import Dispatcher
from loader import bot, db
import middlewares, handlers

async def on_startup():
    print("Bot ishga tushdi!")
    await db.create_table_users()

async def main():
    dp = Dispatcher()
    
    # Register middlewares
    # Note: Middleware registration in v3 is usually done on the dispatcher or router
    # middlewares.setup(dp) -> We refactored this to take dp
    middlewares.setup(dp)

    # Include routers
    dp.include_router(handlers.router)

    # Startup logic
    await on_startup()
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot to'xtatildi")
