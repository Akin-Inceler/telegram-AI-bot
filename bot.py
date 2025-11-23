import logging
import os
import base64
import requests
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

def send_to_n8n(payload: dict):
    """Send event data to n8n webhook for automation/logging."""
    webhook_url = os.getenv("N8N_WEBHOOK_URL")
    if not webhook_url:
        # If webhook not configured, just skip silently
        return

    try:
        requests.post(webhook_url, json=payload, timeout=5)
    except Exception:
        logging.exception("Failed to send data to n8n")


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

    # Send conversation data to n8n for automation/logging
    try:
        send_to_n8n(
            {
                "type": "text",
                "user_id": update.effective_user.id if update.effective_user else None,
                "username": update.effective_user.username if update.effective_user else None,
                "message": user_text,
                "reply": reply,
            }
        )
    except Exception:
        logging.exception("Error calling send_to_n8n from handle_text")

    await update.message.reply_text(reply)


# Photo handler (OpenAI Vision)
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
                            "type": "image_url",
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

    except Exception as e:
        logging.exception("Error while processing image with OpenAI Vision")
        # Geçici debug için istersen hatayı da görebilirsin:
        # reply = f"Error while analyzing the photo: {e}"
        reply = "There was an issue analyzing the photo. Please try again."

        # Send photo analysis data to n8n
    try:
        send_to_n8n(
            {
                "type": "photo",
                "user_id": update.effective_user.id if update.effective_user else None,
                "username": update.effective_user.username if update.effective_user else None,
                "description": reply,
            }
        )
    except Exception:
        logging.exception("Error calling send_to_n8n from handle_photo")

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
