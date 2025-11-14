import logging
import os
import base64
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

# Getting environment variables (set them in Railway or your local terminal)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! 👋 I am your ChatGPT-powered Telegram bot.\n"
        "You can send me text or photos."
    )

# Text handler (ChatGPT-style conversation)
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
                        "You are a friendly English-speaking chatbot inside a Telegram bot. "
                        "Explain things clearly and naturally. Respond in English unless the user uses another language."
                    ),
                },
                {"role": "user", "content": user_text},
            ],
        )

        reply = completion.choices[0].message.content.strip()

    except Exception:
        logging.exception("Error while communicating with OpenAI")
        reply = "Something went wrong while contacting OpenAI. Please try again."

    await update.message.reply_text(reply)

# Photo handler (OpenAI Vision)
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Analyze user photo using OpenAI Vision."""
    photo = update.message.photo[-1]  # highest resolution
    file = await photo.get_file()
    byte_arr = await file.download_as_bytearray()

    # Convert to base64 for OpenAI Vision
    b64_image = base64.b64encode(byte_arr).decode("utf-8")

    await update.message.chat.send_action(action="typing")

    try:
        completion = client.chat.completions.create(
            model="gpt-4.1-mini",   # supports both text + images
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an image analysis assistant. "
                        "Always answer in English, and be concise and clear."
                    ),
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_image",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{b64_image}"
                            },
                        },
                        {
                            "type": "text",
                            "text": (
                                "Please describe this image in a detailed but concise way. "
                                "What do you see? What's the environment? "
                                "Describe objects, mood, and important visual elements."
                            ),
                        },
                    ],
                },
            ],
        )

        reply = completion.choices[0].message.content.strip()

    except Exception:
        logging.exception("Error while processing image with OpenAI Vision")
        reply = "There was an issue analyzing the photo. Please try again."

    await update.message.reply_text(reply)

def main():
    if not TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN environment variable is not set.")

    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY environment variable is not set.")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    app.run_polling()

if __name__ == "__main__":
    main()
