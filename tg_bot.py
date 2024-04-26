import telebot
from telebot import types
import webbrowser
import sqlite3

db = sqlite3.connect('db/blogs.db', check_same_thread=False)
cur = db.cursor()

with open('config.txt', mode='r') as f_in:
    bot = telebot.TeleBot(f_in.read())

@bot.message_handler(commands=['start'])
def hello(message):
  mes = f"<b>{message.from_user.first_name}</b>, привет!\nДобро пожаловать в MailWorld!"
  bot.send_message(message.chat.id, mes, parse_mode='html')
  cur.execute("UPDATE users SET tg_chat = ? WHERE tg_nickname = ?", (message.chat.id, message.chat.username))
  db.commit()

@bot.message_handler(commands=['site'])
def site(message):
    webbrowser.open('http://127.0.0.1:5000//')

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, message.chat.username)

def notification(chat_id, email):
    bot.send_message(chat_id, f'На вашу почту: {email}, пришло новое письмо!')

if __name__ == '__main__':
    bot.send_message(1068181120, 'Бот запущен!  ')
    bot.infinity_polling()