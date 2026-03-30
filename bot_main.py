from config import BOT_TOKEN, PHONE_NUMBERS

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from sheets import Sheets
from database_main import UserDB


#prompts =["Напиши краткий отзыв о том, какая хорошая компания 2Change. Они обменивают валюты и продают eSim. Вставь эмодзи. Объем от 10 до 50 слов"]
db = UserDB()
sh = Sheets()
bot = telebot.TeleBot(BOT_TOKEN)
@bot.message_handler(commands=['start'])
def send_welcome(message, remove_kb=False):
    user_id = message.from_user.id
    chat_id = message.chat.id
    msg = ("🔗Перейдите по этим ссылкам и проставьте оценки 4-5 звезд🔗\n\n"
           "🖼Отчет в виде скринов загрузите в Aviso🖼\n\n"
           
           f"1) Кликните на этот текст чтобы скопировать:\n\n"
           f""
           f"<code>{sh.get_one_review(db.get_used_reviews())}</code>\n\n"
           f""
           f"2) Перейдите по ссылке ниже и разместите отзыв используя скопированный текст"
           ""
           "⏱️Задание доступно раз в 24 часа.\n\n"
           "☝️(Необходимо будет заново зайти через сайт ависо, иначе вы не сможете получить оплату)"
           )
    k = InlineKeyboardMarkup()
    if not db.can_do_task(user_id):
        msg = ("⏱️Новое задание пока недоступно, с момента выполнения прошлого прошло менее чем 24 часа.\n\n"
               "☝️Нужно будет заново зайти через сайт ависо, иначе вы не сможете получить оплату.")
        if not remove_kb:
            k.add(InlineKeyboardButton("Получить задание", callback_data="start"))
        bot.send_message(chat_id, msg, reply_markup=k, parse_mode="HTML")
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

@bot.callback_query_handler(func=lambda call: call.data == "start")
def handle_start(call):
    send_welcome(call.message, True)
    bot.answer_callback_query(call.id)




