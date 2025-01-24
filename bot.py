import telebot

# Bot Token
BOT_TOKEN = "aapka_bot_token"
bot = telebot.TeleBot(BOT_TOKEN)

# File IDs Storage
file_ids = {
    "mp3": None,  # MP3 file_id yahan store hoga
    "mp4": None,  # MP4 file_id yahan store hoga
    "apk": None   # APK file_id yahan store hoga
}

# Start Command
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
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

# Save MP3 File
@bot.message_handler(commands=["setmp3"])
def set_mp3(message):
    bot.reply_to(message, "Please send the MP3 file.")

@bot.message_handler(content_types=["document", "audio"])
def save_file(message):
    if message.content_type == "audio":
        file_ids["mp3"] = message.audio.file_id
        bot.reply_to(message, "MP3 file saved successfully!")
    elif message.content_type == "document":
        file_ids["apk"] = message.document.file_id
        bot.reply_to(message, "APK file saved successfully!")
    else:
        bot.reply_to(message, "File type not supported.")

# Retrieve MP3 File
@bot.message_handler(commands=["mp3"])
def send_mp3(message):
    if file_ids["mp3"]:
        bot.send_audio(message.chat.id, file_ids["mp3"])
    else:
        bot.reply_to(message, "MP3 file not found. Please upload it using /setmp3.")

# Retrieve APK File
@bot.message_handler(commands=["apk"])
def send_apk(message):
    if file_ids["apk"]:
        bot.send_document(message.chat.id, file_ids["apk"])
    else:
        bot.reply_to(message, "APK file not found. Please upload it using /setapk.")

# Polling
if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()
