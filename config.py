import os
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("TOKEN")
os.getenv("TOKEN")

from dotenv import load_dotenv
load_dotenv()

if not TOKEN:
    exit('Error: no token provided')
