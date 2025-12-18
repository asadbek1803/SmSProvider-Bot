import sys
import os
from pathlib import Path

# Add the app directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from data import config
from utils.db_api.sqlite import Database

bot = Bot(
    token=config.BOT_TOKEN, 
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
db = Database()
