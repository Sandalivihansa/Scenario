import logging
import os
import sys
import time
import spamwatch
import httpx
import aiohttp
import psycopg2

from config import Config
from pyrogram import Client, errors
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid, ChannelInvalid
from telethon import TelegramClient
from telethon.sessions import MemorySession, StringSession
from motor import motor_asyncio
from odmantic import AIOEngine
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from redis import StrictRedis
from Python_ARQ import ARQ
from aiohttp import ClientSession
from telegraph import Telegraph
from telegram import Chat, Update
from telegram.ext import Application, CommandHandler, CallbackContext

StartTime = time.time()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

LOGGER = logging.getLogger(__name__)

# Check Python version
if sys.version_info < (3, 6):
    LOGGER.error("Python version must be 3.6 or higher. Bot quitting.")
    sys.exit(1)

ENV = bool(os.environ.get("ENV", False))

if ENV:
    # Load environment variables
    TOKEN = os.environ.get("TOKEN")
    OWNER_ID = int(os.environ.get("OWNER_ID", "1451534504"))
    API_ID = os.environ.get("API_ID")
    API_HASH = os.environ.get("API_HASH")
    DB_URL = os.environ.get("DATABASE_URL")
    MONGO_DB_URL = os.environ.get("MONGO_DB_URL")
    REDIS_URL = os.environ.get("REDIS_URL")
    STRING_SESSION = os.environ.get("STRING_SESSION")
else:
    try:
        from config import Config
        TOKEN = Config.TOKEN
        OWNER_ID = int(Config.OWNER_ID)
        API_ID = Config.API_ID
        API_HASH = Config.API_HASH
        DB_URL = Config.DB_URL
        MONGO_DB_URL = Config.MONGO_DB_URL
        REDIS_URL = Config.REDIS_URL
        STRING_SESSION = Config.STRING_SESSION
    except ImportError as e:
        LOGGER.error(f"Cannot import Config: {e}")
        sys.exit(1)

# Additional configurations
try:
    REDIS = StrictRedis.from_url(REDIS_URL, decode_responses=True)
    REDIS.ping()
    LOGGER.info("Connected to Redis successfully!")
except Exception as e:
    LOGGER.error(f"Error connecting to Redis: {e}")
    sys.exit(1)

try:
    mongodb = MongoClient(MONGO_DB_URL, 27017)
    motor = motor_asyncio.AsyncIOMotorClient(MONGO_DB_URL)
    db = motor["scenario"]
    LOGGER.info("Connected to MongoDB successfully!")
except Exception as e:
    LOGGER.error(f"Error connecting to MongoDB: {e}")
    sys.exit(1)

telegraph = Telegraph()
telegraph.create_account(short_name='ScenarioBot')

# Pyrogram and Telethon setup
telethn = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

# Logging initialization
print("[Scenario] Bot is starting...")
print("[Scenario] Successfully connected!")
print("[Scenario] Maintained by TeamScenario: https://github.com/TeamScenario")

# ARQ client setup
aiohttpsession = ClientSession()
arq = ARQ("https://arq.hamker.in", "YOUR_ARQ_API_KEY", aiohttpsession)

# Helper function to get entities
async def get_entity(client, entity):
    if not isinstance(entity, Chat):
        try:
            entity = int(entity)
        except ValueError:
            pass
        except TypeError:
            entity = entity.id
        try:
            entity = await client.get_chat(entity)
        except (PeerIdInvalid, ChannelInvalid):
            for app in [pgram]:
                try:
                    entity = await app.get_chat(entity)
                    return entity, app
                except (PeerIdInvalid, ChannelInvalid):
                    continue
    return entity, client

# Define the /start command handler
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hello, I'm your bot!")

# Create the Application instance using the token (v20.x+ API)
application = Application.builder().token(TOKEN).build()

# Add handlers
application.add_handler(CommandHandler("start", start))

# Run the bot
application.run_polling()

# Add your initialization code and modules below
from scenario.modules.helper_funcs.handlers import (
    CustomCommandHandler,
    CustomMessageHandler,
    CustomRegexHandler,
)

tg.RegexHandler = CustomRegexHandler
tg.CommandHandler = CustomCommandHandler
tg.MessageHandler = CustomMessageHandler
