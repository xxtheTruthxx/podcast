from dotenv import load_dotenv
import asyncio
import os

# Third-party Dependencies
from aiogram import Bot, Router, Dispatcher    
from aiogram.filters import CommandStart
from aiogram.types import Message

# Load .env variables
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
    """
    Handle /start command.
    """
    await message.answer(
        "Welcome to the PodGen."
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main=main())    