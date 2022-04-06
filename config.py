import os
from os import getenv

from dotenv import load_dotenv

if os.path.exists("local.env"):
    load_dotenv("local.env")

load_dotenv()
admins = {}
SESSION_NAME = getenv("SESSION_NAME", "session")
BOT_TOKEN = getenv("BOT_TOKEN")
BOT_NAME = getenv("BOT_NAME", "Legend Müzik Bot")
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
OWNER_NAME = getenv("OWNER_NAME", "evetbenim38")
ALIVE_NAME = getenv("ALIVE_NAME", "Legend")
BOT_USERNAME = getenv("BOT_USERNAME", "LEGEND_MZK_VDOBOT")
ASSISTANT_NAME = getenv("ASSISTANT_NAME", "lgndasistan")
GROUP_SUPPORT = getenv("GROUP_SUPPORT", "GYCYolcu")
UPDATES_CHANNEL = getenv("UPDATES_CHANNEL", "LegendDestek")
SUDO_USERS = list(map(int, getenv("SUDO_USERS").split()))
COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", "/ ! .").split())
ALIVE_IMG = getenv("ALIVE_IMG", "https://telegra.ph/file/5530445a28dc9e0eaf304.jpg")
DURATION_LIMIT = int(getenv("DURATION_LIMIT", "60"))
UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/Rishabhbhan4/video-Bot")
IMG_1 = getenv("IMG_1", "https://telegra.ph/file/5530445a28dc9e0eaf304.jpg")
IMG_2 = getenv("IMG_2", "https://telegra.ph/file/5530445a28dc9e0eaf304.jpg")
IMG_3 = getenv("IMG_3", "https://telegra.ph/file/5530445a28dc9e0eaf304.jpg")
IMG_4 = getenv("IMG_4", "https://telegra.ph/file/5530445a28dc9e0eaf304.jpg")
