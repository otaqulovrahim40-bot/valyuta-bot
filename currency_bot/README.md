# 💱 O'zbekiston Valyuta Kursi Boti

> **Telegram boti** — O'zbekiston Markaziy Bankining rasmiy API'si asosida real vaqtda valyuta kurslarini ko'rsatuvchi professional bot.

---

## 📁 Loyiha Tuzilmasi

```
currency_bot/
├── main.py                  ← Botni ishga tushirish
├── config.py                ← Sozlamalar va env o'zgaruvchilari
├── requirements.txt         ← Kutubxonalar ro'yxati
├── .env                     ← Bot token (o'zingiz yarating)
├── .env.example             ← .env namunasi
│
├── services/
│   ├── __init__.py
│   └── cbu.py               ← Markaziy Bank API bilan ishlovchi mantiq
│
├── handlers/
│   ├── __init__.py
│   ├── start.py             ← /start va /help buyruqlari
│   └── currency.py          ← Asosiy funksional (kurslar, kalkulyator, tarix)
│
└── keyboards/
    ├── __init__.py
    └── keyboards.py         ← Reply va Inline tugmalar
```

---

## ⚡ Tez Boshlash (Qadam-ba-Qadam)

### 1️⃣ Telegram Botini Yaratish

1. Telegramda **[@BotFather](https://t.me/BotFather)** ga o'ting
2. `/newbot` buyrug'ini yuboring
3. Bot nomini kiriting (masalan: `MyRatesBot`)
4. Bot username'ini kiriting (masalan: `my_rates_bot`)
5. BotFather sizga **API Token** beradi — uni saqlab qo'ying!

---

### 2️⃣ Python O'rnatish

Python **3.10** yoki undan yuqori versiya talab qilinadi.

[python.org](https://python.org/downloads/) dan yuklab o'rnating.

Terminal/CMD da tekshiring:
```bash
python --version
# Python 3.10+ bo'lishi kerak
```

---

### 3️⃣ Loyihani Sozlash

```bash
# Loyiha papkasiga o'tish
cd currency_bot

# Virtual muhit yaratish (tavsiya etiladi)
python -m venv venv

# Virtual muhitni faollashtirish:
# Windows uchun:
venv\Scripts\activate
# Linux/Mac uchun:
source venv/bin/activate

# Kutubxonalarni o'rnatish
pip install -r requirements.txt
```

---

### 4️⃣ .env Faylini Yaratish

`currency_bot/` papkasida `.env` nomli fayl yarating:

```env
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

> ⚠️ `BOT_TOKEN` ni BotFather'dan olgan tokeningiz bilan almashtiring!

---

### 5️⃣ Botni Ishga Tushirish

```bash
python main.py
```

Muvaffaqiyatli ishga tushganda:
```
2024-01-15 10:30:00 [INFO] __main__: ✅ Bot muvaffaqiyatli ishga tushdi!
2024-01-15 10:30:00 [INFO] __main__: 🤖 Botni to'xtatish uchun Ctrl+C bosing
```

---

## 🎯 Bot Funksionalligi

| Tugma / Buyruq | Tavsif |
|---|---|
| `/start` | Botni ishga tushirish, asosiy menyuni ko'rsatish |
| `/help` | Yordam va foydalanish qo'llanmasi |
| `/rates` | Bugungi valyuta kurslarini ko'rsatish |
| `/calc` | Valyuta kalkulyatorini ochish |
| `/history` | Haftalik kurs tarixini ko'rsatish |
| `💵 Bugungi kurslar` | USD, EUR, RUB, CNY kurslarini chiroyli formatda |
| `🧮 Valyuta kalkulyatori` | Ixtiyoriy summani valyutaga o'girish |
| `📈 O'zgarishlar tarixi` | So'nggi 7 kunlik kurs grafigi |
| `⚙️ Sozlamalar` | Bot sozlamalari |

---

## 📦 Kutubxonalar

| Kutubxona | Versiya | Maqsad |
|---|---|---|
| `aiogram` | 3.7.0 | Telegram Bot Framework |
| `aiohttp` | 3.9.5 | Asinxron HTTP so'rovlar |
| `python-dotenv` | 1.0.1 | .env faylidan o'zgaruvchilarni o'qish |

---

## 🔧 Muammolar va Yechimlar

### ❌ `BOT_TOKEN .env faylida topilmadi!`
→ `.env` fayl yaratilganini va tokenni to'g'ri kiritganingizni tekshiring.

### ❌ `ModuleNotFoundError`
→ `pip install -r requirements.txt` buyrug'ini qayta ishlatib ko'ring.

### ❌ Kurslar ko'rinmayapti
→ Internet ulanishini tekshiring. CBU API vaqtincha ishlamayotgan bo'lishi mumkin.

### ❌ `Conflict: terminated by other getUpdates request`
→ Bot allaqachon boshqa joyda ishlamoqda. Barcha sessiyalarni yoping.

---

## 🌐 API Haqida

Bot **O'zbekiston Markaziy Banki**ning ochiq API'sidan foydalanadi:
- URL: `https://cbu.uz/uz/arkhiv-kursov-valyut/json/`
- Muayyan sana: `https://cbu.uz/uz/arkhiv-kursov-valyut/json/YYYY-MM-DD/`
- Litsenziya: Ochiq ma'lumotlar (CBU rasmiy sayti)

---

## 👨‍💻 Texnologiyalar

- **Python 3.10+**
- **aiogram 3.x** (asinxron Telegram bot framework)
- **aiohttp** (asinxron HTTP klient)
- **FSM** (Finite State Machine — kalkulyator holatlari uchun)
- **python-dotenv** (xavfsiz konfiguratsiya)

---

*Muvaffaqiyatli ishlatishingizni tilaymiz! 🚀*
