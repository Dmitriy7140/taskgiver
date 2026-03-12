from config import BOT_TOKEN
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from sheets import Sheets
from database_main import UserDB

db = UserDB()
sh = Sheets()
bot = telebot.TeleBot(BOT_TOKEN)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    msg = ("🔗Перейдите по этим ссылкам и проставьте оценки 4-5 звезд🔗\n\n"
           "🖼Отчет в виде скринов загрузите в Aviso🖼\n\n"
           ""
           "Задание доступно раз в 24 часа"
           )
    k = InlineKeyboardMarkup()
    if not db.can_do_task(user_id):
        msg = "Новое задание пока недоступно, с момента выполнения прошлого прошло менее чем 24 часа."
        bot.send_message(chat_id, msg)
        return
    links = sh.get_random_three(used_links=db.get_user_links(user_id))
    if not links:
        msg = "Нет доступных ссылок, повторите попытку позже."
        bot.send_message(chat_id, msg)
        return

    for i, link in enumerate(links, start=1):
        k.add(InlineKeyboardButton(f"Ссылка {i}", url=link))
    bot.send_message(chat_id, msg, reply_markup=k)
    db.update_last_task(user_id)
    db.add_user_links(user_id, links)
    return
