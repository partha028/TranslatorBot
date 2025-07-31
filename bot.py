import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from googletrans import Translator
from indic_transliteration.sanscript import transliterate, ITRANS, DEVANAGARI

translator = Translator()

def roman_to_hindi(text):
    try:
        return transliterate(text, ITRANS, DEVANAGARI)
    except Exception:
        return text

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hi! Reply to any message with /translate to get English translation."
    )

def translate_command(update: Update, context: CallbackContext):
    # Check if this message is a reply
    if update.message.reply_to_message:
        roman_text = update.message.reply_to_message.text
        if not roman_text:
            update.message.reply_text("⚠️ The replied message has no text to translate.")
            return

        try:
            # Step 1: Transliterate Roman script to Hindi script
            devanagari_text = roman_to_hindi(roman_text)

            # Step 2: Translate from Hindi to English
            translated = translator.translate(devanagari_text, src='hi', dest='en')

            reply_text = f"🗣️ Original: {roman_text}\n🔤 Translation: {translated.text}"
            update.message.reply_text(reply_text)
        except Exception as e:
            update.message.reply_text(f"⚠️ Translation failed: {str(e)}")
    else:
        update.message.reply_text("💬 Please reply to a message you want to translate.")

def main():
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        print("Error: BOT_TOKEN environment variable not set.")
        return

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("translate", translate_command))

    print("🤖 Bot is running...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
