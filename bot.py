from telebot import *
from repository import *
from information import *

token = "6815594086:AAFmwexlJBjfNt8xinJKVhUz2613ND2opX0"
bot = TeleBot(token=token)


def markup_create(index):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(len(quest[index]["answer"])):
        markup.add(types.KeyboardButton(quest[index]["answer"][i]))
    return markup


@bot.message_handler(commands=["start"])
def start_quest(message):
    markup = markup_create(-1)
    bot.send_message(chat_id=message.chat.id, text="Вы начали квест", reply_markup=markup)
    start_json_file(message)
    msg = bot.reply_to(message, f"{quest[-1]['text']}")
    bot.send_photo(message.chat.id, open(quest[-1]["photo"], "rb"))
    bot.register_next_step_handler(msg, response_processing)


def response_processing(message):
    data = open_json_file_and_write()
    if message.text in quest[data["users"][message.chat.username]["index"][-1]]["answer"]:
        index = answer.index(message.text)
        data['users'][message.chat.username]['index'].append(index)
        save_json_file_and_write(data)
        bot.send_message(chat_id=message.chat.id, text=quest[index]["text"], reply_markup=types.ReplyKeyboardRemove())
        bot.send_photo(message.chat.id, open(quest[index]["photo"], "rb"))
        if len(data["users"][message.chat.username]["index"]) == 3:
            bot.send_message(chat_id=message.chat.id, text="Квест Окончен")
        else:
            markup = markup_create(index)
            msg = bot.reply_to(message, f"{quest[index]['text']}", reply_markup=markup)
            bot.register_next_step_handler(msg, response_processing)
    else:
        bot.send_message(chat_id=message.chat.id, text="Вы написали чепуху, переделайте ответ")
        msg = bot.reply_to(message, text=quest[data['users'][message.chat.username]['index'][-1]]['text'])
        bot.send_photo(message.chat.id, open(quest[data['users'][message.chat.username]['index'][-1]]["photo"], "rb"))
        bot.register_next_step_handler(msg, response_processing)


@bot.message_handler(commands=["help"])
def help_items(message):
    bot.send_message(chat_id=message.chat.id, text="Помогаю")


@bot.message_handler(content_types=["text"])
def incorrect_input(message):
    bot.send_message(chat_id=message.chat.id, text="Такой команды не существует.")


bot.polling()
