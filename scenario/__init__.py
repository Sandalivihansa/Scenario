import logging
import os
import sys
import time
import spamwatch
import httpx
import aiohttp
import telegram.ext as tg
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
    LOGGER.error(
        "You MUST have a Python version of at least 3.6! Multiple features depend on this. Bot quitting."
    )
    sys.exit(1)

# Environment setup
ENV = bool(os.environ.get("ENV", False))

# Helper function to parse integers from environment variables safely
def parse_env_int(key, default=None):
    value = os.environ.get(key, default)
    try:
        return int(value) if value else default
    except ValueError:
        raise Exception(f"The environment variable {key} must be a valid integer.")

if ENV:
    TOKEN = os.environ.get("TOKEN")
    if not TOKEN:
        raise Exception("TOKEN environment variable is missing.")

    OWNER_ID = parse_env_int("OWNER_ID", 2142595466)

    JOIN_LOGGER = os.environ.get("EVENT_LOGS")
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME", "CoderX")

    DRAGONS = {parse_env_int(x) for x in os.environ.get("DRAGONS", "").split() if x}
    DEV_USERS = {parse_env_int(x) for x in os.environ.get("DEV_USERS", "").split() if x}
    DEMONS = {parse_env_int(x) for x in os.environ.get("DEMONS", "").split() if x}
    WOLVES = {parse_env_int(x) for x in os.environ.get("WOLVES", "").split() if x}
    TIGERS = {parse_env_int(x) for x in os.environ.get("TIGERS", "").split() if x}

    INFOPIC = os.environ.get("INFOPIC", "True").lower() in ["true", "1"] or "https://telegra.ph/file/a9ec99487ecd550460309.jpg"
    EVENT_LOGS = os.environ.get("EVENT_LOGS")
    ERROR_LOGS = os.environ.get("ERROR_LOGS")
    WEBHOOK = os.environ.get("WEBHOOK", "False").lower() in ["true", "1"]
    URL = os.environ.get("URL", "")
    PORT = parse_env_int("PORT", 8443)
    CERT_PATH = os.environ.get("CERT_PATH")
    API_ID = parse_env_int("API_ID")
    API_HASH = os.environ.get("API_HASH")
    DB_URL = os.environ.get("DATABASE_URL")

    if DB_URL:
        DB_URL = DB_URL.replace("postgres://", "postgresql://", 1)
        connection_db = psycopg2.connect(DB_URL, sslmode="require")

    DONATION_LINK = os.environ.get("DONATION_LINK", "https://t.me/i_14344")
    WORKERS = parse_env_int("WORKERS", 8)
    MONGO_DB_URL = os.environ.get("MONGO_DB_URL")
    REDIS_URL = os.environ.get("REDIS_URL")
    SPAMWATCH_API = os.environ.get("SPAMWATCH_API")

else:
    TOKEN = Config.TOKEN
    OWNER_ID = parse_env_int(Config.OWNER_ID)
    OWNER_USERNAME = Config.OWNER_USERNAME
    DRAGONS = {parse_env_int(x) for x in Config.DRAGONS or []}
    DEV_USERS = {parse_env_int(x) for x in Config.DEV_USERS or []}
    DEMONS = {parse_env_int(x) for x in Config.DEMONS or []}
    WOLVES = {parse_env_int(x) for x in Config.WOLVES or []}
    TIGERS = {parse_env_int(x) for x in Config.TIGERS or []}
    INFOPIC = Config.INFOPIC
    EVENT_LOGS = Config.EVENT_LOGS
    ERROR_LOGS = Config.ERROR_LOGS
    WEBHOOK = Config.WEBHOOK
    URL = Config.URL
    PORT = Config.PORT
    CERT_PATH = Config.CERT_PATH
    API_ID = parse_env_int(Config.API_ID)
    API_HASH = Config.API_HASH
    DB_URL = Config.DB_URL
    MONGO_DB_URL = Config.MONGO_DB_URL
    REDIS_URL = Config.REDIS_URL
    SPAMWATCH_API = Config.SPAMWATCH_API

# Setup Redis connection
REDIS = StrictRedis.from_url(REDIS_URL, decode_responses=True)
try:
    REDIS.ping()
    LOGGER.info("[Scenario]: Connected to Redis.")
except Exception as e:
    raise Exception(f"[Scenario ERROR]: Redis connection failed! {e}")

# Setup SpamWatch
if SPAMWATCH_API:
    try:
        sw = spamwatch.Client(SPAMWATCH_API)
    except Exception as e:
        sw = None
        LOGGER.warning(f"[Scenario ERROR]: SpamWatch connection failed! {e}")
else:
    sw = None
    LOGGER.warning("[Scenario ERROR]: SpamWatch API key missing.")

# Setup MongoDB
print("[Scenario]: Connecting to MongoDB")
mongodb = MongoClient(MONGO_DB_URL, 27017)
motor = motor_asyncio.AsyncIOMotorClient(MONGO_DB_URL)
db = motor["scenario"]
engine = AIOEngine(motor, "scenario")

# Setup ARQ client
print("[Scenario]: Initializing ARQ client")
aiohttpsession = ClientSession()
arq = ARQ("https://arq.hamker.in", "WAYBIT-TMRYKK-YUHERI-RLDXRI-ARQ", aiohttpsession)

# Bot initialization
telegraph = Telegraph()
telegraph.create_account(short_name="Scenario")
updater = tg.Updater(
    token=TOKEN,
    base_url=os.environ.get('BOT_API_URL', 'https://api.telegram.org/bot'),
    workers=WORKERS
)
telethn = TelegramClient(MemorySession(), API_ID, API_HASH)
dispatcher = updater.dispatcher
pgram = Client(session_name=TOKEN.split(":")[0], api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)

# Final setup
LOGGER.info("[Scenario]: All systems initialized.")
