import logging
import os
from io import BytesIO

from PIL import Image
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from openai import OpenAI

# Ortam değişkenlerinden alıyoruz (terminalde set edeceksin)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# /start komutu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Merhaba! 👋 Ben ChatGPT destekli Telegram botunum.\n"
        "Bana metin ya da fotoğraf gönderebilirsin."
    )

# Metin handler (ChatGPT ile sohbet)
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    await update.message.chat.send_action(action="typing")

    try:
        completion = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a friendly Turkish chatbot talking inside a Telegram bot. "
                        "Explain things clearly and briefly, and feel free to answer in Turkish "
                        "unless the user clearly writes in another language."
                    ),
                },
                {"role": "user", "content": user_text},
            ],
        )

        reply = completion.choices[0].message.content.strip()

    except Exception:
        logging.exception("Error while talking to OpenAI")
        reply = "Şu an OpenAI ile konuşurken bir hata oldu, lütfen biraz sonra tekrar dene."

    await update.message.reply_text(reply)

# Fotoğraf handler (şimdilik sadece boyut bilgisi)
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await photo.get_file()
    byte_arr = await file.download_as_bytearray()

    img = Image.open(BytesIO(byte_arr))
    width, height = img.size

    description = f"{width}x{height} boyutunda bir görsel aldım. Mode: {img.mode}"
    await update.message.reply_text("Fotoğraf için teşekkürler! " + description)

def main():
    if not TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN ortam değişkeni tanımlı değil.")

    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY ortam değişkeni tanımlı değil.")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    app.run_polling()

if __name__ == "__main__":
    main()
