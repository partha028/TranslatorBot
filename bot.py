import logging
import filetype
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from googletrans import Translator

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Instantiate the translator
translator = Translator()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Send me a message and I'll translate it to Hindi.")

async def translate_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    original_text = update.message.text
    translated = translator.translate(original_text, dest='hi')
    await update.message.reply_text(f"Translated:\n{translated.text}")

# Example usage of filetype in your bot (optional for images)
def is_image(file_path):
    kind = filetype.guess(file_path)
    return kind and kind.mime.startswith('image/')

def main():
    app = ApplicationBuilder().token("8142191151:AAE4sjqeHNhP2Hk7UDsKpK8Jew-FTrqNkd0").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate_message))

    app.run_polling()

if __name__ == "__main__":
    main()
