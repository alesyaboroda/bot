import re
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
async def read(update: Update, context: ContextTypes.DEFAULT_TYPE):
    b = re.search('1', update.message.text)
    c = b.start()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=a[c:])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

if __name__ == '__main__':
    application = ApplicationBuilder().token('5575413400:AAFhVO28r2RS9x6V3S1z4eYjUooBbqLLALQ').build()
    read_handler = ReadHandler()
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    application.run_polling()
