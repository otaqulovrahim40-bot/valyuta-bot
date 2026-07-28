from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from services.cbu import (
    get_today_rates,
    get_week_history,
    format_rate_message,
    format_history_message,
)
from keyboards.keyboards import (
    main_menu,
    calculator_currency_kb,
    history_currency_kb,
    back_to_menu_kb,
    settings_kb,
)
from config import CURRENCY_FLAGS, CURRENCY_NAMES, MAIN_CURRENCIES

router = Router()


# ─── FSM States ──────────────────────────────────────────────────────────────

class CalcState(StatesGroup):
    waiting_currency = State()
    waiting_amount = State()


# ─── Bugungi kurslar ─────────────────────────────────────────────────────────

@router.message(F.text == "💵 Bugungi kurslar")
@router.message(Command("rates"))
async def show_rates(message: Message):
    wait_msg = await message.answer("⏳ <i>Kurslar yuklanmoqda...</i>")
    rates = await get_today_rates()
    if not rates:
        await wait_msg.edit_text(
            "❌ <b>Xatolik yuz berdi!</b>\n\n"
            "Markaziy bank API'siga ulanishda muammo bor.\n"
            "Iltimos, bir necha soniyadan so'ng qaytadan urinib ko'ring.",
            reply_markup=back_to_menu_kb(),
        )
        return
    text = format_rate_message(rates)
    await wait_msg.edit_text(text, reply_markup=back_to_menu_kb())


# ─── Valyuta Kalkulyatori ────────────────────────────────────────────────────

@router.message(F.text == "🧮 Valyuta kalkulyatori")
@router.message(Command("calc"))
async def show_calculator(message: Message, state: FSMContext):
    await state.set_state(CalcState.waiting_currency)
    await message.answer(
        "🧮 <b>Valyuta Kalkulyatori</b>\n\n"
        "Qaysi valyutaga hisoblashni xohlaysiz?\n"
        "Quyidagi valyutalardan birini tanlang:",
        reply_markup=calculator_currency_kb(),
    )


@router.callback_query(F.data.startswith("calc:"), CalcState.waiting_currency)
async def calc_choose_currency(callback: CallbackQuery, state: FSMContext):
    code = callback.data.split(":")[1]
    await state.update_data(currency=code)
    await state.set_state(CalcState.waiting_amount)
    flag = CURRENCY_FLAGS.get(code, "🏳️")
    await callback.message.edit_text(
        f"💱 <b>{flag} {code} kalkulyatori</b>\n\n"
        f"Endi hisoblashni xohlagan summani kiriting:\n\n"
        f"<b>Misol:</b> <code>100</code> yoki <code>1500000</code>\n\n"
        f"💡 <i>UZS summa kiritsangiz — {code}'ga, "
        f"{code} summa kiritsangiz — UZS'ga o'giriladi</i>",
    )
    await callback.answer()


@router.message(CalcState.waiting_amount)
async def calc_compute(message: Message, state: FSMContext):
    raw = message.text.strip().replace(",", ".").replace(" ", "")
    try:
        amount = float(raw)
        if amount <= 0:
            raise ValueError
    except ValueError:
        await message.answer(
            "⚠️ <b>Noto'g'ri format!</b>\n\n"
            "Iltimos, faqat musbat raqam kiriting.\n"
            "<b>Misol:</b> <code>100</code> yoki <code>50000</code>",
            reply_markup=back_to_menu_kb(),
        )
        return

    data = await state.get_data()
    code = data.get("currency", "USD")
    await state.clear()

    rates = await get_today_rates()
    rate_info = rates.get(code)

    if not rate_info:
        await message.answer(
            f"❌ <b>{code}</b> kursi topilmadi. Keyinroq urinib ko'ring.",
            reply_markup=back_to_menu_kb(),
        )
        return

    rate = rate_info["rate"]
    nominal = rate_info["nominal"]
    rate_per_unit = rate / nominal
    flag = CURRENCY_FLAGS.get(code, "🏳️")

    # Har ikki yo'nalishda hisob
    uzs_amount = amount * rate_per_unit
    foreign_amount = amount / rate_per_unit

    # Boshqa valyutalarga ham
    cross_lines = []
    for other in MAIN_CURRENCIES:
        if other == code:
            continue
        other_info = rates.get(other)
        if not other_info:
            continue
        other_rate = other_info["rate"] / other_info["nominal"]
        other_flag = CURRENCY_FLAGS.get(other, "🏳️")
        cross = amount * rate_per_unit / other_rate
        cross_lines.append(f"  {other_flag} <b>{other}:</b> <code>{cross:,.4f}</code>")

    cross_text = "\n".join(cross_lines) if cross_lines else ""

    text = (
        f"🧮 <b>Valyuta Hisob-Kitobi</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{flag} <b>{amount:,.2f} {code}</b>\n"
        f"  ➡️ <code>{uzs_amount:,.2f}</code> <b>UZS (so'm)</b>\n\n"
        f"🇺🇿 <b>{amount:,.2f} UZS</b>\n"
        f"  ➡️ <code>{foreign_amount:,.6f}</code> <b>{code}</b>\n"
    )

    if cross_text:
        text += f"\n🔄 <b>{amount:,.2f} {code} boshqa valyutalarda:</b>\n{cross_text}\n"

    text += (
        f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📌 <i>1 {code} = {rate_per_unit:,.2f} so'm (CBU kursi)</i>\n"
        f"🔄 Yangi hisob uchun yana raqam kiriting yoki menyuga qayting."
    )

    await message.answer(text, reply_markup=back_to_menu_kb())


# ─── Haftalik Tarix ──────────────────────────────────────────────────────────

@router.message(F.text == "📈 O'zgarishlar tarixi")
@router.message(Command("history"))
async def show_history_menu(message: Message):
    await message.answer(
        "📈 <b>So'nggi 7 kunlik tarix</b>\n\n"
        "Qaysi valyuta kursini ko'rishni xohlaysiz?",
        reply_markup=history_currency_kb(),
    )


@router.callback_query(F.data.startswith("hist:"))
async def show_history(callback: CallbackQuery):
    code = callback.data.split(":")[1]
    await callback.message.edit_text(
        f"⏳ <i>{code} tarixi yuklanmoqda (7 kun)...</i>\n"
        f"<i>Bu biroz vaqt olishi mumkin</i>"
    )
    history = await get_week_history(code)
    text = format_history_message(code, history)
    await callback.message.edit_text(text, reply_markup=back_to_menu_kb())
    await callback.answer()


# ─── Sozlamalar ──────────────────────────────────────────────────────────────

@router.message(F.text == "⚙️ Sozlamalar")
async def show_settings(message: Message):
    await message.answer(
        "⚙️ <b>Sozlamalar</b>\n\n"
        "Quyidagi imkoniyatlar mavjud:",
        reply_markup=settings_kb(),
    )


# ─── Callback handlers ───────────────────────────────────────────────────────

@router.callback_query(F.data == "back_menu")
async def back_to_main(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(
        "🏠 <b>Asosiy menyu</b>\n\nKerakli bo'limni tanlang:",
        reply_markup=main_menu(),
    )
    await callback.answer()


@router.callback_query(F.data == "soon")
async def coming_soon(callback: CallbackQuery):
    await callback.answer("🚧 Ushbu funksiya tez kunda qo'shiladi!", show_alert=True)


# ─── Noto'g'ri xabar ─────────────────────────────────────────────────────────

@router.message()
async def unknown_message(message: Message, state: FSMContext):
    current = await state.get_state()
    if current == CalcState.waiting_amount:
        await calc_compute(message, state)
        return
    await message.answer(
        "🤔 <b>Tushunmadim.</b>\n\n"
        "Iltimos, quyidagi menyudan tanlang yoki /help buyrug'ini ishlating.",
        reply_markup=main_menu(),
    )
