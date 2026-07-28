from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from config import MAIN_CURRENCIES, CURRENCY_FLAGS


def main_menu() -> ReplyKeyboardMarkup:
    """Asosiy menyu tugmalari."""
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="💵 Bugungi kurslar"),
        KeyboardButton(text="🧮 Valyuta kalkulyatori"),
    )
    builder.row(
        KeyboardButton(text="📈 O'zgarishlar tarixi"),
        KeyboardButton(text="⚙️ Sozlamalar"),
    )
    return builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Menyu bandini tanlang...",
    )


def calculator_currency_kb() -> InlineKeyboardMarkup:
    """Kalkulyator uchun valyuta tanlash klaviaturasi."""
    builder = InlineKeyboardBuilder()
    for code in MAIN_CURRENCIES:
        flag = CURRENCY_FLAGS.get(code, "🏳️")
        builder.button(text=f"{flag} {code}", callback_data=f"calc:{code}")
    builder.adjust(2)
    return builder.as_markup()


def history_currency_kb() -> InlineKeyboardMarkup:
    """Tarix uchun valyuta tanlash klaviaturasi."""
    builder = InlineKeyboardBuilder()
    for code in MAIN_CURRENCIES:
        flag = CURRENCY_FLAGS.get(code, "🏳️")
        builder.button(text=f"{flag} {code}", callback_data=f"hist:{code}")
    builder.adjust(2)
    return builder.as_markup()


def back_to_menu_kb() -> InlineKeyboardMarkup:
    """Asosiy menyuga qaytish tugmasi."""
    builder = InlineKeyboardBuilder()
    builder.button(text="🏠 Asosiy menyu", callback_data="back_menu")
    return builder.as_markup()


def settings_kb() -> InlineKeyboardMarkup:
    """Sozlamalar klaviaturasi."""
    builder = InlineKeyboardBuilder()
    builder.button(text="🔔 Bildirishnomalar (tez kunda)", callback_data="soon")
    builder.button(text="📌 Valyutalarni tanlash (tez kunda)", callback_data="soon")
    builder.button(text="🏠 Asosiy menyu", callback_data="back_menu")
    builder.adjust(1)
    return builder.as_markup()
