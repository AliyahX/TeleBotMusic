import os
import yt_dlp
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your actual bot token
TELEGRAM_BOT_TOKEN = os.getenv('7271834580:AAEQxjMXilZbRGp5TAAhQ6ljJ0wLj5wJ9VI')

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! Send me a YouTube link, and I will download the audio for you.')

def download_song(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    update.message.reply_text('Downloading... Please wait.')

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info_dict).replace('.webm', '.mp3')
    
    update.message.reply_text('Download complete! Sending the file...')
    update.message.reply_audio(audio=open(file_path, 'rb'))
    os.remove(file_path)

def main() -> None:
    updater = Updater(TELEGRAM_BOT_TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, download_song))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
