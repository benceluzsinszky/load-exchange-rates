import os
import requests
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, db

load_dotenv()
api_key = os.getenv("API_KEY")
exchange_url = f"https://openexchangerates.org/api/latest.json?app_id={api_key}"
response = requests.get(exchange_url, timeout=5)

if response.status_code == 200:
    rates = response.json()["rates"]

if not firebase_admin._apps:
    database_url = os.getenv("DATABASE_URL")
    cred = credentials.Certificate('credentials.json')
    firebase_admin.initialize_app(
        cred,
        {"databaseURL": database_url})

    ref = db.reference()
    ref.set(rates)

    firebase_admin.delete_app(firebase_admin.get_app())
