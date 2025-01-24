import os
import telebot
import json

# Bot Token
BOT_TOKEN = "8189093263:AAGKQcoNuKMpNzJdW7tAQVBXuNJbkFVnqsw"
bot = telebot.TeleBot(BOT_TOKEN)

# Bot Owner ID
OWNER_ID = 7408008545  # Replace this with your Telegram user ID

# List of Sudo Users
SUDO_USERS = [7256617868]  # Add Telegram User IDs of Sudo Users here

# File IDs storage
file_ids = {}

# Save File IDs to JSON
def save_file_ids():
    with open("file_ids.json", "w") as f:
        json.dump(file_ids, f)

# Load File IDs from JSON
def load_file_ids():
    global file_ids
    try:
        with open("file_ids.json", "r") as f:
            file_ids = json.load(f)
    except FileNotFoundError:
        file_ids = {"mp3": None, "mp4": None, "apk": None}

# Load file IDs at startup
load_file_ids()

# Check if user is authorized (Owner or Sudo User)
def is_authorized(user_id):
    return user_id == OWNER_ID or user_id in SUDO_USERS

# Start Command
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    if is_authorized(message.from_user.id):
        bot.reply_to(
            message,
            "Welcome! Use the following commands:\n"
            "/setmp3 - Upload MP3 file\n"
            "/setmp4 - Upload MP4 file\n"
            "/setapk - Upload APK file\n"
            "/mp3 - Get MP3 file\n"
            "/mp4 - Get MP4 file\n"
            "/apk - Get APK file"
        )
    else:
        bot.reply_to(message, "Welcome! Use this bot to access files.")

# Save MP3 file (Authorized users only)
@bot.message_handler(commands=["setmp3"])
def set_mp3(message):
    if is_authorized(message.from_user.id):
        bot.reply_to(message, "Please send the MP3 file.")
    else:
        bot.reply_to(message, "You are not authorized to upload files.")

# Save MP4 file (Authorized users only)
@bot.message_handler(commands=["setmp4"])
def set_mp4(message):
    if is_authorized(message.from_user.id):
        bot.reply_to(message, "Please send the MP4 file.")
    else:
        bot.reply_to(message, "You are not authorized to upload files.")

# Save APK file (Authorized users only)
@bot.message_handler(commands=["setapk"])
def set_apk(message):
    if is_authorized(message.from_user.id):
        bot.reply_to(message, "Please send the APK file.")
    else:
        bot.reply_to(message, "You are not authorized to upload files.")

# Handle file uploads (Authorized users only)
@bot.message_handler(content_types=["document", "audio", "video"])
def save_file(message):
    if is_authorized(message.from_user.id):
        if message.content_type == "audio":
            file_ids["mp3"] = message.audio.file_id
            bot.reply_to(message, "MP3 file saved successfully!")
        elif message.content_type == "document" and message.document.mime_type == "application/vnd.android.package-archive":
            file_ids["apk"] = message.document.file_id
            bot.reply_to(message, "APK file saved successfully!")
        elif message.content_type == "video":
            file_ids["mp4"] = message.video.file_id
            bot.reply_to(message, "MP4 file saved successfully!")
        else:
            bot.reply_to(message, "File type not supported.")
        save_file_ids()
    else:
        bot.reply_to(message, "You are not authorized to upload files.")

# Retrieve MP3 file
@bot.message_handler(commands=["mp3"])
def send_mp3(message):
    if file_ids.get("mp3"):
        bot.send_audio(message.chat.id, file_ids["mp3"])
    else:
        bot.reply_to(message, "MP3 file not found.")

# Retrieve MP4 file
@bot.message_handler(commands=["mp4"])
def send_mp4(message):
    if file_ids.get("mp4"):
        bot.send_video(message.chat.id, file_ids["mp4"])
    else:
        bot.reply_to(message, "MP4 file not found.")

# Retrieve APK file
@bot.message_handler(commands=["apk"])
def send_apk(message):
    if file_ids.get("apk"):
        bot.send_document(message.chat.id, file_ids["apk"])
    else:
        bot.reply_to(message, "APK file not found.")

# Start polling
if __name__ == "__main__":
    print("Bot is running...")
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"Error: {e}")
