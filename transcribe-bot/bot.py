"""Бот-расшифровщик: превращает голосовые, кружки, видео и аудио в текст
и отвечает на сообщение расшифровкой.

Работает двумя способами:
  1. Как обычный бот в групповом чате (добавить в группу, см. README.md).
  2. Как бизнес-бот в ВАШИХ личных переписках (Telegram Premium ->
     Настройки -> Telegram для бизнеса -> Чат-боты). Тогда бот расшифровывает
     сообщения собеседников и ваши в переписках, где вы его разрешили.

Распознавание речи — локально (faster-whisper), ключи и платные API не нужны.
"""
import asyncio
import logging
import os
import tempfile
from pathlib import Path

from faster_whisper import WhisperModel
from telegram import Message, Update
from telegram.constants import ChatAction
from telegram.error import TelegramError
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

MODEL_SIZE = os.getenv("WHISPER_MODEL", "small")      # tiny/base/small/medium/large-v3
LANGUAGE = os.getenv("WHISPER_LANGUAGE") or None      # напр. "ru"; пусто = определять автоматически
ALLOWED_CHATS = {int(x) for x in os.getenv("ALLOWED_CHATS", "").replace(" ", "").split(",") if x}
MAX_FILE_MB = 20                                      # лимит Telegram Bot API на скачивание
MAX_TEXT = 4000                                       # лимит длины сообщения Telegram — 4096

logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.INFO)
log = logging.getLogger("transcribe-bot")

_model: WhisperModel | None = None


def get_model() -> WhisperModel:
    global _model
    if _model is None:
        log.info("Загружаю модель whisper '%s'...", MODEL_SIZE)
        _model = WhisperModel(MODEL_SIZE, device="auto", compute_type="int8")
    return _model


def transcribe(path: str) -> str:
    segments, _info = get_model().transcribe(
        path, language=LANGUAGE, vad_filter=True, beam_size=5
    )
    return " ".join(s.text.strip() for s in segments).strip()


def pick_media(msg: Message):
    """Возвращает объект с файлом (voice/video_note/video/audio/документ-медиа) или None."""
    for media in (msg.voice, msg.video_note, msg.video, msg.audio):
        if media:
            return media
    doc = msg.document
    if doc and doc.mime_type and doc.mime_type.startswith(("audio/", "video/")):
        return doc
    return None


async def on_media(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.effective_message
    if msg is None:
        return
    if ALLOWED_CHATS and msg.chat_id not in ALLOWED_CHATS:
        return
    media = pick_media(msg)
    if media is None:
        return
    if media.file_size and media.file_size > MAX_FILE_MB * 1024 * 1024:
        await msg.reply_text(f"Файл больше {MAX_FILE_MB} МБ — Telegram не даёт боту его скачать.")
        return

    try:
        await msg.chat.send_action(ChatAction.TYPING)
    except TelegramError:
        pass

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "media"
        try:
            tg_file = await context.bot.get_file(media.file_id)
            await tg_file.download_to_drive(path)
            # распознавание тяжёлое — выносим из event loop
            text = await asyncio.to_thread(transcribe, str(path))
        except Exception:
            log.exception("Не удалось расшифровать")
            await msg.reply_text("⚠️ Не получилось расшифровать это сообщение.")
            return

    if not text:
        await msg.reply_text("🎙 Речь не распознана.")
        return
    for i in range(0, len(text), MAX_TEXT):
        await msg.reply_text(("🎙 " if i == 0 else "") + text[i:i + MAX_TEXT])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_message.reply_text(
        "Я расшифровываю голосовые, кружки, видео и аудио в текст.\n"
        "Добавьте меня в чат — я отвечу текстом под каждым таким сообщением."
    )


def main() -> None:
    app = Application.builder().token(os.environ["BOT_TOKEN"]).build()
    media_filter = (
        filters.VOICE | filters.VIDEO_NOTE | filters.VIDEO | filters.AUDIO
        | filters.Document.AUDIO | filters.Document.VIDEO
    )
    app.add_handler(CommandHandler("start", start, filters=filters.ChatType.PRIVATE))
    # обычные чаты/группы
    app.add_handler(MessageHandler(media_filter, on_media))
    # бизнес-режим (личные переписки аккаунта Premium)
    app.add_handler(MessageHandler(media_filter & filters.UpdateType.BUSINESS_MESSAGES, on_media))
    get_model()  # прогрев: скачает модель при первом запуске
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
