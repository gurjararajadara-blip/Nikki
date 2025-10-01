
import os
import requests
from telegram import InputFile
from telegram.ext import CallbackContext
from telegram.update import Update

def download_from_url(url: str, dest_path: str):
    """URL से file download करके dest_path पर save करो"""
    with requests.get(url, stream=True, timeout=30) as r:
        r.raise_for_status()
        with open(dest_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

def handle_url(update: Update, context: CallbackContext):
    text = update.message.text.strip()
    chat_id = update.effective_chat.id

    if not (text.startswith("http://") or text.startswith("https://")):
        return  # URL नहीं है

    context.bot.send_message(chat_id=chat_id, text=f"🔄 Downloading: {text}")

    try:
        filename = text.split("/")[-1] or "downloaded_file"
        os.makedirs("temp_downloads", exist_ok=True)
        temp_path = os.path.join("temp_downloads", filename)

        download_from_url(text, temp_path)

        with open(temp_path, "rb") as f:
            context.bot.send_document(chat_id=chat_id, document=f)

        os.remove(temp_path)

    except Exception as e:
        context.bot.send_message(chat_id=chat_id, text=f"⚠️ Error: {e}")
