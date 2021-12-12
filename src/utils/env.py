import os
from dotenv import load_dotenv
load_dotenv()


class vars:
    TOKEN = os.getenv("TOKEN")
    ADMIN = os.getenv("ADMIN")
