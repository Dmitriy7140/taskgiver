from config import BOT_TOKEN, PHONE_NUMBERS
import random
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
           f"<b>НОМЕР ТЕЛЕФОНА:</b> {random.choice(PHONE_NUMBERS)}"
           ""
           "⏱️Задание доступно раз в 24 часа.\n\n"
           "☝️(Необходимо будет заново зайти через сайт ависо, иначе вы не сможете получить оплату)"
           )
    k = InlineKeyboardMarkup()
    if not db.can_do_task(user_id):
        msg = ("⏱️Новое задание пока недоступно, с момента выполнения прошлого прошло менее чем 24 часа.\n\n"
               "☝️Нужно будет заново зайти через сайт ависо, иначе вы не сможете получить оплату.")
        bot.send_message(chat_id, msg)
        return
    link = sh.get_random_link(db.get_used_links())
    if not link:
        msg = "Нет доступных ссылок, повторите попытку позже."
        bot.send_message(chat_id, msg)
        return


    k.add(InlineKeyboardButton(f"Ссылка", url=link))
    bot.send_message(chat_id, msg, reply_markup=k, parse_mode="HTML")

    db.add_used_link(link, user_id)
    return
