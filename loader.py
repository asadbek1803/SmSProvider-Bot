import sys
import os
from pathlib import Path

from environs import Env

# Add the app directory to Python path
sys.path.insert(0, str(Path(__file__).parent))




env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS", subcast=int)

from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from utils.db_api.sqlite import Database

bot = Bot(
    token=BOT_TOKEN, 
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
db = Database()
