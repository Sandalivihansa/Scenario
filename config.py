import os

class Config:
    """
    Configuration class for storing bot settings and environment variables.
    """

    # Token from botfather 
    TOKEN = os.environ.get("YOUR_BOT_TOKEN", "7332398186:AAHG5L3MF-8BtP4ouR_9a_T2tBgje_GegN0")

    # Make a new group then add @ScenarioXbot then send /id and fill id here.
    JOIN_LOGGER = os.environ.get("JOIN_LOGGER", "-1002325247996")

    # Only one # don't remove other one.
    OWNER_ID = int(os.environ.get("OWNER_ID", "1451534504"))

    # Only one # don't remove other one.
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME", "CoderX")

    # Can add multiple with spaces
    DRAGONS = {int(x) for x in os.environ.get("DRAGONS", "").split()}

    # Can add multiple with spaces
    DEV_USERS = {int(x) for x in os.environ.get("DEV_USERS", "").split()}

    # Can add multiple with spaces
    DEMONS = {int(x) for x in os.environ.get("DEMONS", "").split()} 

    # Can add multiple with spaces
    WOLVES = {int(x) for x in os.environ.get("WOLVES", "").split()}

    # Can add multiple with spaces
    TIGERS = {int(x) for x in os.environ.get("TIGERS", "").split()}

    # Should I show profile pic of user in /info command? Default value is true
    INFOPIC = bool(os.environ.get("INFOPIC", True)) or "https://telegra.ph/file/a9ec99487ecd550460309.jpg"

    # Make a new group then add @ScenarioXbot then send /id and fill id here.
    EVENT_LOGS = os.environ.get("EVENT_LOGS", None)

    # Make a new group then add @ScenarioXbot then send /id and fill id here.
    ERROR_LOGS = os.environ.get("ERROR_LOGS", None)

    # Don't touch if you don't know.
    WEBHOOK = bool(os.environ.get("WEBHOOK", False))

    # Heroku app url
    URL = os.environ.get("URL", "")  # If You Deploy On Heroku. [URL Example: https://{appname}.herokuapp.com/]
    PORT = int(os.environ.get("PORT", 8443))

    CERT_PATH = os.environ.get("CERT_PATH")

    # Bot Owner's API_ID (From: https://my.telegram.org/apps)
    API_ID = os.environ.get("API_ID", "5047271")

    # Bot Owner's API_HASH (From: https://my.telegram.org/apps)
    API_HASH = os.environ.get("API_HASH", "047d9ed308172e637d4265e1d9ef0c27")

    # Any SQL Database Link (Recommended: PostgreSQL)
    DB_URL = os.environ.get("DATABASE_URL", "") 

    # Don't touch
    DB_URL = DB_URL.replace("postgres://", "postgresql://", 1)

    # Donation Link (Optional)
    DONATION_LINK = os.environ.get("DONATION_LINK", "https://t.me/i_14344")

    # Wall API key for wallpapers (From: https://wall.alphacoders.com/api.php)
    WALL_API = os.environ.get("WALL_API", None)

    # To remove background of images (From: https://www.remove.bg/)
    REM_BG_API_KEY = os.environ.get("REM_BG_API_KEY", "qV26c84dUAhUuEb3sG9N9M9Q")

    # More info
    OPENWEATHERMAP_ID = os.environ.get("OPENWEATHERMAP_ID", "")  # From: https://openweathermap.org/api
    GENIUS_API_TOKEN = os.environ.get("GENIUS_API_TOKEN", None)  # From: http://genius.com/api-clients

    # Database connection URL (MongoDB example)
    MONGO_DB_URL = os.environ.get("MONGO_DB_URL", "mongodb+srv://Cluster006:600510@cluster006.ootpa.mongodb.net/Cluster006?retryWrites=true&w=majority")
    REDIS_URL = os.environ.get("REDIS_URL", "redis://Madharjoot:GuKhao123_@redis-12276.c275.us-east-1-4.ec2.cloud.redislabs.com:12276/Madharjoot")

    # Telegram Bot ID
    BOT_ID = int(os.environ.get("BOT_ID", "7332398186"))

    # Support Chat Group Link
    SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", None) 

    # SpamWatch API (optional)
    SPAMWATCH_SUPPORT_CHAT = os.environ.get("SPAMWATCH_SUPPORT_CHAT", None)
    SPAMWATCH_API = os.environ.get("SPAMWATCH_API", None)

    # Bot Username
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "@testingplate45_bot")

    # String Session (Telethon)
    STRING_SESSION = os.environ.get("STRING_SESSION", None)

    # Repo and Developer Information
    REPO = "TeamScenario/Scenario"
    DEVELOPER = "TeamScenario"

    # API keys and URLs
    ARQ_API_URL = "https://arq.hamker.in"
    GOOGLE_CHROME_BIN = "/usr/bin/google-chrome"
    CHROME_DRIVER = "/usr/bin/chromedriver"
    SUDO_USERS = "2142595466"
    WHITELIST_USERS = "2142595466"
    BOT_API_URL = os.environ.get('BOT_API_URL', "https://api.telegram.org/bot")
    UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", "TeamScenario")

    # Images for help and group start
    HELP_IMG = os.environ.get("HELP_IMG", True) or "https://telegra.ph/file/a9ec99487ecd550460309.jpg"
    GROUP_START_IMG = os.environ.get("GROUP_START_IMG", True) or "https://telegra.ph/file/a9ec99487ecd550460309.jpg"
    SCENARIO_PIC = os.environ.get("SCENARIO_PIC", True) or "https://telegra.ph/file/a9ec99487ecd550460309.jpg"

    # Blacklist Chats
    BL_CHATS = {int(x) for x in os.environ.get("BL_CHATS", "").split()}

    # Other settings
    LOAD = os.environ.get("LOAD", "").split()
    NO_LOAD = os.environ.get("NO_LOAD", "translation").split()

    # Enable/disable command deletion
    DEL_CMDS = bool(os.environ.get("DEL_CMDS", False))

    # Strict GBan
    STRICT_GBAN = bool(os.environ.get("STRICT_GBAN", False)) or "True"

    # Bot Workers
    WORKERS = int(os.environ.get("WORKERS", 8))

    # Sticker ID for banning
    BAN_STICKER = os.environ.get("BAN_STICKER", "")

    # Exclusions
    ALLOW_EXCL = os.environ.get("ALLOW_EXCL", False)

    # Download directory
    TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TEMP_DOWNLOAD_DIRECTORY", "./")

    # Cash API Key
    CASH_API_KEY = os.environ.get("CASH_API_KEY", None) or "70F3DVSKF6RUAHQV"

    # Time API Key
    TIME_API_KEY = os.environ.get("TIME_API_KEY", None) or "K5PTMFOEC82M"
