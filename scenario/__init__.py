import logging
import os
import sys
import time
import spamwatch
import httpx
import aiohttp
import telegram.ext as tg
import psycopg2

from pyrogram import Client
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid, ChannelInvalid
from telethon import TelegramClient
from telethon.sessions import MemorySession, StringSession
from motor import motor_asyncio
from odmantic import AIOEngine
from pymongo import MongoClient
from redis import StrictRedis
from Python_ARQ import ARQ
from aiohttp import ClientSession
from telegraph import Telegraph
from telegram import Chat

StartTime = time.time()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)
LOGGER = logging.getLogger(__name__)

# Ensure Python version compatibility
if sys.version_info < (3, 6):
    LOGGER.error("Python 3.6 or higher is required. Bot quitting.")
    sys.exit(1)

# Load environment variables
ENV = bool(os.environ.get("ENV", False))

if ENV:
    # Mandatory environment variables
    TOKEN = os.environ.get("TOKEN")
    if not TOKEN:
        raise Exception("TOKEN environment variable is missing.")

    try:
        OWNER_ID = int(os.environ.get("OWNER_ID", "0"))
    except ValueError:
        raise Exception("OWNER_ID must be an integer.")

    API_ID = os.environ.get("API_ID")
    API_HASH = os.environ.get("API_HASH")
    if not API_ID or not API_HASH:
        raise Exception("API_ID and API_HASH are required environment variables.")

    # Optional environment variables with defaults
    EVENT_LOGS = os.environ.get("EVENT_LOGS", None)
    MONGO_DB_URL = os.environ.get("MONGO_DB_URL", "")
    REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    STRING_SESSION = os.environ.get("STRING_SESSION", None)
else:
    from config import Config

    TOKEN = Config.TOKEN
    OWNER_ID = int(Config.OWNER_ID)
    API_ID = Config.API_ID
    API_HASH = Config.API_HASH
    EVENT_LOGS = Config.EVENT_LOGS
    MONGO_DB_URL = Config.MONGO_DB_URL
    REDIS_URL = Config.REDIS_URL
    STRING_SESSION = Config.STRING_SESSION

# Initialize Redis
REDIS = StrictRedis.from_url(REDIS_URL, decode_responses=True)
try:
    REDIS.ping()
    LOGGER.info("Connected to Redis.")
except Exception as e:
    LOGGER.error(f"Failed to connect to Redis: {e}")
    sys.exit(1)

# Initialize SpamWatch
SPAMWATCH_API = os.environ.get("SPAMWATCH_API", None)
if SPAMWATCH_API:
    try:
        sw = spamwatch.Client(SPAMWATCH_API)
        LOGGER.info("Connected to SpamWatch API.")
    except Exception as e:
        sw = None
        LOGGER.warning(f"Failed to connect to SpamWatch API: {e}")
else:
    sw = None
    LOGGER.warning("SpamWatch API key is missing.")

# Initialize Telegraph
telegraph = Telegraph()
telegraph.create_account(short_name="Scenario")

# Initialize Telegram Clients
updater = tg.Updater(
    token=TOKEN,
    workers=8,
    use_context=True
)
telethn = TelegramClient(MemorySession(), API_ID, API_HASH)
pgram = Client(
    TOKEN.split(":"),
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=TOKEN,
)

# Initialize MongoDB
if MONGO_DB_URL:
    try:
        mongodb = MongoClient(MONGO_DB_URL)["scenario"]
        motor = motor_asyncio.AsyncIOMotorClient(MONGO_DB_URL)
        db = motor["scenario"]
        engine = AIOEngine(motor, "scenario")
        LOGGER.info("Connected to MongoDB.")
    except Exception as e:
        LOGGER.error(f"Failed to connect to MongoDB: {e}")
        sys.exit(1)
else:
    LOGGER.warning("MongoDB URL is missing. Some features may not work.")

# Initialize ARQ Client
aiohttpsession = ClientSession()
arq = ARQ("https://arq.hamker.in", "WAYBIT-TMRYKK-YUHERI-RLDXRI-ARQ", aiohttpsession)

# Initialize Telethon Userbot
if STRING_SESSION:
    ubot = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
else:
    ubot = None
    LOGGER.warning("STRING_SESSION is missing. Userbot features will be disabled.")

# Additional Functions and Configurations
def add_to_set(env_var):
    try:
        return {int(x) for x in os.environ.get(env_var, "").split()}
    except ValueError:
        LOGGER.warning(f"Invalid integers in {env_var}. Using empty set.")
        return set()

DRAGONS = add_to_set("DRAGONS") | {OWNER_ID}
DEV_USERS = add_to_set("DEV_USERS") | {OWNER_ID}
DEMONS = add_to_set("DEMONS")
WOLVES = add_to_set("WOLVES")
TIGERS = add_to_set("TIGERS")

# Credits Logger
LOGGER.info("Scenario Bot is starting. Maintained by https://github.com/TeamScenario.")

# Import Handlers
from scenario.modules.helper_funcs.handlers import (
    CustomCommandHandler,
    CustomMessageHandler,
    CustomRegexHandler,
)
tg.RegexHandler = CustomRegexHandler
tg.CommandHandler = CustomCommandHandler
tg.MessageHandler = CustomMessageHandler
