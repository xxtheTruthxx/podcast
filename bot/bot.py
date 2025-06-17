from dotenv import load_dotenv
import asyncio
import os

# Third-party Dependencies
from aiogram import Bot, Router, Dispatcher    
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import aiohttp

# Local Dependencies
from helper.utils import logger

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
        "Welcome to the PodGen.\nCheck commands: /help"
    )

@router.message(Command("help"))
async def help_command(message: Message):
    """
    Handle /help command.
    """
    await message.reply(
        """
        Use /alt <episode_id> <target> <prompt> to generate alternative titles of description.
        \nArgs:\n
        \t<episode_id> - number
        \t<target> - `title` or `description`
        \t<prompt> - prompt
        \nExample: /alt 1 title Rewrite the title for GenZ.
        """
    )

@router.message(Command("alt"))
async def alt_command(message: Message):
    try:
        parts = message.text.split(maxsplit=3)
        if len(parts) < 3:
            await message.reply(
                "Please provide: /alt <episode_id> <target> <prompt>"
            )
            return
        _, episode_id, target, prompt = parts

        # Validate episode_id:
        if not episode_id.isdigit():
            await message.reply(
                "The <episode id> must be a number."
            )

        url = f"http://localhost:8000/api/v1/podcast/episodes/{episode_id}/generate_alternative"
        data = {
            "target": target,
            "prompt": prompt 
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                if response.status == 200:
                    result = await response.json(encoding="utf-8")
                    alternative = result.get("generated_alternative", "No alternative generated.")
                    await message.reply(alternative)
                else:
                    await message.reply(f"Unexpected status code: {response.status}.")
    except aiohttp.ClientError as err:
        logger.error(f"HTTP Request failed: {err}")
        await message.reply("There was issue connecting to the server.")
    except Exception as err:
        logger.error(f"Unexpected error: {err}")
        await message.reply("An unexpected error occurred.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main=main())    