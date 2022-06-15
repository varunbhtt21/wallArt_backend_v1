from dotenv import load_dotenv
from os.path import join, dirname
import os



dotenv_path = join(dirname(__file__), ".env")
load_dotenv(override=True)

API_KEY = os.environ.get("API_KEY_test")
API_SECRET = os.environ.get("API_SECRET_test")