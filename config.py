import os
#TOKEN = "5963306703:AAEwm-sz59B3HXe9UYdGJsqjO_TN0_YnIn4"
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("TOKEN")
os.getenv("TOKEN")

from dotenv import load_dotenv
load_dotenv()

if not TOKEN:
    exit('Error: no token provided')