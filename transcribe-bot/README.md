# Бот-расшифровщик голосовых и видео

Отвечает текстом на голосовые, кружки, видео и аудиофайлы. Речь распознаётся локально (faster-whisper).

## Запуск
```bash
pip install -r requirements.txt
export BOT_TOKEN="токен от @BotFather"
export WHISPER_LANGUAGE=ru      # необязательно, иначе язык определяется сам
export WHISPER_MODEL=small      # tiny/base/small/medium/large-v3 — точнее, но медленнее
export ALLOWED_CHATS=-100123,456  # необязательно: только эти chat_id
python bot.py
```
При первом запуске скачается модель (small ≈ 480 МБ).

## Подключение
**Группа:** добавьте бота в чат. Чтобы он видел все сообщения, в @BotFather: `/mybots` → бот → Bot Settings → Group Privacy → **Turn off**, затем удалите бота из группы и добавьте снова.

**Ваши личные переписки (нужен Telegram Premium):** @BotFather → Bot Settings → **Business Mode** → включить. Затем в Telegram: Настройки → Telegram для бизнеса → Чат-боты → выберите бота и укажите, в каких чатах он работает.

## Ограничения
- Telegram даёт боту скачивать файлы до 20 МБ.
- В обычных секретных чатах и звонках бот не работает.
