import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN .env faylida topilmadi! Iltimos, .env faylini to'ldiring.")

# CBU API
CBU_API_URL = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"

# Asosiy valyutalar
MAIN_CURRENCIES = ["USD", "EUR", "RUB", "CNY"]

# Valyuta bayroqlari va nomlari
CURRENCY_FLAGS = {
    "USD": "🇺🇸",
    "EUR": "🇪🇺",
    "RUB": "🇷🇺",
    "CNY": "🇨🇳",
    "GBP": "🇬🇧",
    "JPY": "🇯🇵",
    "KZT": "🇰🇿",
    "KGS": "🇰🇬",
    "TRY": "🇹🇷",
    "AED": "🇦🇪",
}

CURRENCY_NAMES = {
    "USD": "AQSh dollari",
    "EUR": "Evro",
    "RUB": "Rossiya rubli",
    "CNY": "Xitoy yuani",
    "GBP": "Britaniya funt sterlingi",
    "JPY": "Yaponiya iyenasi",
    "KZT": "Qozogʻiston tengesi",
    "KGS": "Qirgʻiziston somi",
    "TRY": "Turk lirasi",
    "AED": "BAA dirhami",
}
