from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from keyboards.keyboards import main_menu

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    name = message.from_user.first_name or "Foydalanuvchi"
    await message.answer(
        f"🎉 <b>Assalomu alaykum, {name}!</b>\n\n"
        f"💱 Men <b>O'zbekiston Markaziy Banki</b> ma'lumotlariga asoslanuvchi "
        f"<b>Valyuta Kursi Botiman</b>.\n\n"
        f"📌 <b>Nima qila olaman?</b>\n"
        f"• 💵 Bugungi valyuta kurslarini ko'rsatish\n"
        f"• 🧮 Valyuta konvertatsiyasi hisoblash\n"
        f"• 📈 Haftalik kurs o'zgarishini tahlil qilish\n\n"
        f"⬇️ Quyidagi menyudan kerakli bo'limni tanlang:",
        reply_markup=main_menu(),
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "📖 <b>Foydalanish qo'llanmasi</b>\n\n"
        "🔹 /start — Botni ishga tushirish\n"
        "🔹 /rates — Bugungi kurslar\n"
        "🔹 /calc — Valyuta kalkulyatori\n"
        "🔹 /history — Haftalik tarix\n\n"
        "💡 <b>Maslahat:</b> Kalkulyator rejimida shunchaki raqam yozing, "
        "bot avtomatik hisoblaydi!",
        reply_markup=main_menu(),
    )
