from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from googletrans import Translator
from indic_transliteration.sanscript import transliterate, ITRANS, DEVANAGARI
import os

translator = Translator()

def roman_to_hindi(text):
    try:
        return transliterate(text, ITRANS, DEVANAGARI)
    except:
        return text

async def translate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        roman_text = update.message.reply_to_message.text
        try:
            devanagari_text = roman_to_hindi(roman_text)
            translated = translator.translate(devanagari_text, src='hi', dest='en')
            await update.message.reply_text(f"🗣️ Original: {roman_text}\n🔤 Translation: {translated.text}")
        except Exception as e:
            await update.message.reply_text("⚠️ Translation failed.")
    else:
        await update.message.reply_text("💬 Please reply to a message you want to translate.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Reply to any message with /translate to get English translation.")

if __name__ == '__main__':
    TOKEN = os.getenv("BOT_TOKEN")  # Secure: Use environment variable
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("translate", translate_command))
    app.run_polling()
