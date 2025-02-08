from os import getenv

from dotenv import load_dotenv

load_dotenv()


API_ID = int(getenv("API_ID", 29405214))
API_HASH = getenv("API_HASH", "7696243cee1a03564f70cfe74f70e729")

BOT_TOKEN = getenv("BOT_TOKEN", "8031625217:AAFbgiBXi0BtkATt5ptynq1e-GGlf6gmGkI")
MONGO_DB_URI = getenv("MONGO_DB_URI", "mongodb+srv://hamadtep:hamad@cluster0.1tmgm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

OWNER_ID = int(getenv("OWNER_ID", 1490479382))
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/n_nnae")
