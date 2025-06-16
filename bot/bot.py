from dotenv import load_dotenv
import asyncio
import os

from aiogram import Bot, Router, Dispatcher    
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from helpers.utils import HTTPRequest

# load .env variables
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Create a router for handling messages 
router = Router()
dp.include_router(router) 

@router.message(CommandStart())
async def start(message: Message):
    message.answer(
        "Hello"
    )
    # async with HTTPRequest("https://api.ipify.org/") as http:
        # data = await http.get()
        # print(data)

# Main function to run the bot
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main=main())    