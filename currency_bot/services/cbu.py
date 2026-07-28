import aiohttp
from datetime import datetime, timedelta
from typing import Optional
from config import CBU_API_URL, CURRENCY_FLAGS, CURRENCY_NAMES, MAIN_CURRENCIES


async def fetch_rates(date: Optional[str] = None) -> list[dict]:
    """
    CBU API'dan valyuta kurslarini olish.
    date format: "YYYY-MM-DD" (bo'sh bo'lsa bugungi kurs olinadi)
    """
    url = CBU_API_URL
    if date:
        url = f"https://cbu.uz/uz/arkhiv-kursov-valyut/json/{date}/"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 200:
                    data = await resp.json(content_type=None)
                    return data
                return []
    except Exception:
        return []


async def get_today_rates() -> dict[str, dict]:
    """Bugungi kurslarni qaytaradi."""
    raw = await fetch_rates()
    result = {}
    for item in raw:
        code = item.get("Ccy", "")
        result[code] = {
            "rate": float(item.get("Rate", 0)),
            "diff": float(item.get("Diff", 0)),
            "name": item.get("CcyNm_UZ", CURRENCY_NAMES.get(code, code)),
            "nominal": int(item.get("Nominal", 1)),
        }
    return result


async def get_rate_for_currency(code: str) -> Optional[dict]:
    """Bitta valyuta kursini qaytaradi."""
    rates = await get_today_rates()
    return rates.get(code.upper())


async def get_week_history(code: str) -> list[dict]:
    """
    So'nggi 7 kunlik kurs tarixi.
    Returns: [{"date": "...", "rate": ..., "diff": ...}, ...]
    """
    history = []
    today = datetime.now()
    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        raw = await fetch_rates(date_str)
        for item in raw:
            if item.get("Ccy") == code.upper():
                history.append({
                    "date": date.strftime("%d.%m.%Y"),
                    "rate": float(item.get("Rate", 0)),
                    "diff": float(item.get("Diff", 0)),
                })
                break
    return history


def format_rate_message(rates: dict[str, dict]) -> str:
    """Asosiy valyutalar uchun chiroyli xabar yaratadi."""
    today = datetime.now().strftime("%d.%m.%Y")
    lines = [
        f"📊 <b>Valyuta Kurslari</b>",
        f"🗓 <i>{today} holatiga ko'ra</i>",
        f"🏦 <b>Manba: O'zbekiston Markaziy Banki</b>",
        "━" * 28,
    ]

    for code in MAIN_CURRENCIES:
        info = rates.get(code)
        if not info:
            continue
        flag = CURRENCY_FLAGS.get(code, "🏳️")
        rate = info["rate"]
        diff = info["diff"]
        nominal = info["nominal"]

        if diff > 0:
            trend = f"📈 +{diff:,.2f}"
        elif diff < 0:
            trend = f"📉 {diff:,.2f}"
        else:
            trend = "➡️ 0.00"

        nom_str = f"{nominal} " if nominal > 1 else ""
        lines.append(
            f"{flag} <b>{nom_str}{code}</b> = <code>{rate:,.2f}</code> so'm\n"
            f"    {trend} so'm (kecha nisbatan)"
        )
        lines.append("─" * 28)

    lines.append("\n🔄 <i>Kurslar real vaqtda yangilanadi</i>")
    return "\n".join(lines)


def format_history_message(code: str, history: list[dict]) -> str:
    """Haftalik tarix uchun xabar."""
    flag = CURRENCY_FLAGS.get(code, "🏳️")
    name = CURRENCY_NAMES.get(code, code)
    lines = [
        f"📈 <b>{flag} {code} — Haftalik tarix</b>",
        f"<i>{name}</i>",
        "━" * 28,
    ]

    if not history:
        return f"❌ <b>{code}</b> uchun tarix ma'lumoti topilmadi."

    for entry in history:
        date = entry["date"]
        rate = entry["rate"]
        diff = entry["diff"]
        if diff > 0:
            trend = f"📈 +{diff:,.2f}"
        elif diff < 0:
            trend = f"📉 {diff:,.2f}"
        else:
            trend = "➡️"
        lines.append(f"📅 <b>{date}</b>: <code>{rate:,.2f}</code> so'm  {trend}")

    # Min/max hisob
    rates_only = [e["rate"] for e in history]
    if rates_only:
        lines.append("━" * 28)
        lines.append(f"📊 <b>Eng yuqori:</b> <code>{max(rates_only):,.2f}</code> so'm")
        lines.append(f"📊 <b>Eng past:</b> <code>{min(rates_only):,.2f}</code> so'm")
        diff_total = rates_only[-1] - rates_only[0]
        sign = "+" if diff_total >= 0 else ""
        lines.append(f"📊 <b>Haftalik o'zgarish:</b> <code>{sign}{diff_total:,.2f}</code> so'm")

    return "\n".join(lines)
