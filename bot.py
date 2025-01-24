from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot's token (replace with your actual token)
TOKEN = 'YOUR_BOT_API_TOKEN'

# Command to send APK file (local or Google Drive link)
def send_apk(update: Update, context):
    apk_link = 'https://drive.google.com/your_file_link'
    update.message.reply_text(f"Here is the APK file: {apk_link}")

# Command to send MP3 file (local or Google Drive link)
def send_mp3(update: Update, context):
    mp3_link = 'https://drive.google.com/your_mp3_file_link'
    update.message.reply_text(f"Here is the MP3 file: {mp3_link}")

# Command to send MP4 file (local or Google Drive link)
def send_mp4(update: Update, context):
    mp4_link = 'https://drive.google.com/your_mp4_file_link'
    update.message.reply_text(f"Here is the MP4 video: {mp4_link}")

# Function to handle file upload
def handle_file(update: Update, context):
    file = update.message.document  # This will fetch the file sent by the user
    file_name = file.file_name
    file_id = file.file_id

    # Get the file from Telegram servers
    new_file = context.bot.get_file(file_id)

    # Create a directory to save files (if it doesn't exist)
    if not os.path.exists('received_files'):
        os.makedirs('received_files')

    # Define the file path where you want to save the file
    file_path = os.path.join('received_files', file_name)

    # Download the file to the specified path
    new_file.download(file_path)

    # Acknowledge the user
    update.message.reply_text(f'File "{file_name}" has been uploaded successfully!')

# Command to start the bot
def start(update: Update, context):
    update.message.reply_text('Hello! Use the commands to get the files:\n'
                              '/apk - Get APK file\n'
                              '/mp3 - Get MP3 audio file\n'
                              '/mp4 - Get MP4 video file\n'
                              'Send me a file to upload it.')

def main():
    # Set up the Updater
    updater = Updater(TOKEN, use_context=True)
    
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('apk', send_apk))
    dispatcher.add_handler(CommandHandler('mp3', send_mp3))
    dispatcher.add_handler(CommandHandler('mp4', send_mp4))

    # Register message handler for receiving files
    dispatcher.add_handler(MessageHandler(Filters.document, handle_file))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
