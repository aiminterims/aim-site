"""Телеграм-бот: собирает телефон и email, сохраняет в Excel (leads.xlsx).

Запуск:
    export BOT_TOKEN="токен от @BotFather"
    export ADMIN_IDS="123456789"        # необязательно: кто может выгружать таблицу (/export)
    python bot.py
"""
import logging
import os
import re
import threading
from datetime import datetime
from pathlib import Path

from openpyxl import Workbook, load_workbook
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application, CommandHandler, ContextTypes, ConversationHandler,
    MessageHandler, filters,
)

XLSX_PATH = Path(os.getenv("XLSX_PATH", "leads.xlsx"))
ADMIN_IDS = {int(x) for x in os.getenv("ADMIN_IDS", "").replace(" ", "").split(",") if x}
HEADERS = ["Дата", "Telegram ID", "Username", "Имя", "Телефон", "Email"]

PHONE, EMAIL = range(2)
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]{2,}$")
_lock = threading.Lock()

logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.INFO)


def normalize_phone(text: str) -> str | None:
    """Возвращает телефон в виде +XXXXXXXXXXX или None, если формат неверный."""
    digits = re.sub(r"\D", "", text)
    if not 10 <= len(digits) <= 15:
        return None
    if len(digits) == 11 and digits[0] == "8":  # 8XXXXXXXXXX -> +7XXXXXXXXXX
        digits = "7" + digits[1:]
    return "+" + digits


def save_row(row: list) -> None:
    with _lock:
        if XLSX_PATH.exists():
            wb = load_workbook(XLSX_PATH)
            ws = wb.active
        else:
            wb = Workbook()
            ws = wb.active
            ws.title = "Заявки"
            ws.append(HEADERS)
            for col, w in zip("ABCDEF", (19, 14, 18, 22, 18, 30)):
                ws.column_dimensions[col].width = w
        ws.append(row)
        # телефон храним текстом, чтобы Excel не превращал его в число
        ws.cell(ws.max_row, 5).number_format = "@"
        wb.save(XLSX_PATH)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    kb = ReplyKeyboardMarkup(
        [[KeyboardButton("📱 Отправить мой номер", request_contact=True)]],
        resize_keyboard=True, one_time_keyboard=True,
    )
    await update.message.reply_text(
        "Здравствуйте! Оставьте контакты, и мы свяжемся с вами.\n\n"
        "Нажмите кнопку ниже или введите номер телефона вручную.",
        reply_markup=kb,
    )
    return PHONE


async def got_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    msg = update.message
    raw = msg.contact.phone_number if msg.contact else msg.text
    phone = normalize_phone(raw or "")
    if not phone:
        await msg.reply_text("Не похоже на номер телефона. Пример: +7 900 123-45-67")
        return PHONE
    context.user_data["phone"] = phone
    await msg.reply_text("Спасибо! Теперь введите ваш email:", reply_markup=ReplyKeyboardRemove())
    return EMAIL


async def got_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    email = update.message.text.strip()
    if not EMAIL_RE.match(email):
        await update.message.reply_text("Некорректный email. Пример: name@example.com")
        return EMAIL
    u = update.effective_user
    save_row([
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        u.id, f"@{u.username}" if u.username else "", u.full_name,
        context.user_data["phone"], email,
    ])
    context.user_data.clear()
    await update.message.reply_text("Готово, данные сохранены. Спасибо! 🙌\nЧтобы отправить заново: /start")
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    await update.message.reply_text("Отменено. Для начала заново: /start", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


async def export(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/export — прислать Excel-файл (только для ADMIN_IDS)."""
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("Нет доступа.")
        return
    if not XLSX_PATH.exists():
        await update.message.reply_text("Данных пока нет.")
        return
    with _lock, XLSX_PATH.open("rb") as f:
        await update.message.reply_document(f, filename=XLSX_PATH.name)


def main() -> None:
    token = os.environ["BOT_TOKEN"]
    app = Application.builder().token(token).build()
    app.add_handler(ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            PHONE: [MessageHandler(filters.CONTACT | (filters.TEXT & ~filters.COMMAND), got_phone)],
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, got_email)],
        },
        fallbacks=[CommandHandler("cancel", cancel), CommandHandler("start", start)],
    ))
    app.add_handler(CommandHandler("export", export))
    app.run_polling()


if __name__ == "__main__":
    main()
