from dotenv import load_dotenv
import os
import selenium

load_dotenv()

url = os.getenv("guru-url")
username = os.getenv("guru-username")
password = os.getenv("guru-password")
