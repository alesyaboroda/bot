import logging
import re
import sqlite3
import json
from telegram import Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler
conn = sqlite3.connect('test.db')
cur = conn.cursor()
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

'''
cur.execute("""CREATE TABLE IF NOT EXISTS people
    (NAME TEXT  PRIMARY KEY,
    AGE INT);""")

cur.execute("""INSERT INTO people(NAME, AGE) VALUES(?, ?);""", ('gogi bobi', 2,))
cur.execute("""INSERT INTO people(NAME, AGE) VALUES(?, ?);""", ('petr pupkin', 3,))
conn.commit()

name = ('Алексей Ханинëв')
cur.execute("""SELECT * FROM people WHERE NAME = ?;""", (name,))
one_result = cur.fetchone()
print(one_result)

cur.execute("""UPDATE people set AGE = ? where NAME = ?;""", (4, name,))
conn.commit()
cur.execute("""SELECT * FROM people WHERE NAME = ?;""", (name,))
two_result = cur.fetchone()
print(two_result)

conn.close()
'''

async def read(update: Update, context: ContextTypes.DEFAULT_TYPE):
    thing = re.search('сумма дней на след неделе занято:', update.message.text)
    conn = sqlite3.connect('test.db')
    cur = conn.cursor()
    if bool(thing) == True:
        days = update.message.text[int(thing.end()):]
        name = str(update.effective_user.first_name) + ' ' + str(update.effective_user.last_name)
        cur.execute('''SELECT NAME FROM people WHERE NAME = ?;''', (name,))
        if len(cur.fetchall()) != 0:
            cur.execute('''UPDATE people set AGE = ? where NAME = ?;''', (days, name,))
            cur.execute('''SELECT * FROM people WHERE NAME = ?''', (name,))
            print('updated ', cur.fetchone())
            conn.commit()
        else:
            cur.execute('''INSERT INTO people(NAME, AGE) VALUES(?, ?);''', (name, days,))
            cur.execute('''SELECT * FROM people WHERE NAME = ?''', (name,))
            print('added ', cur.fetchone())
            conn.commit()

    conn.close()
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = sqlite3.connect('test.db')
    cur = conn.cursor()
    with conn:
        cur.execute("SELECT * FROM people")
        text = (cur.fetchall())
        for row in text:
            print (str(row))
    conn.close()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=str(text))


if __name__ == '__main__':
    application = ApplicationBuilder().token('5575413400:AAFhVO28r2RS9x6V3S1z4eYjUooBbqLLALQ').build()
    read_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), read)
    start_handler = CommandHandler('start', start)
    info_handler = CommandHandler('info', info)
    application.add_handler(start_handler)
    application.add_handler(read_handler)
    application.add_handler(info_handler)
    application.run_polling()