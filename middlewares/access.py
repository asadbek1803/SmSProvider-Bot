from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from loader import db
from data.config import ADMINS

class AccessMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        user = event.from_user
        if not user:
             return await handler(event, data) 

        # Add user to DB (or ignore if exists)
        await db.add_user(telegram_id=user.id, full_name=user.full_name)
        
        # Fetch user info
        user_data = await db.select_user(telegram_id=user.id)
        
        # user table: (id, telegram_id, full_name, is_access)
        is_access = user_data[3]

        if user.id not in ADMINS and not is_access:
            await event.answer("Sizga botdan foydalanishga ruxsat berilmagan. Admin bilan bog'laning.")
            return # Block execution
            
        return await handler(event, data)
