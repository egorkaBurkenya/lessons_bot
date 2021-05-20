from config import token
import telebot
from telebot import types
import json

with open("lessons.json", "r") as file:
    lessons = json.load(file)




bot = telebot.TeleBot(token)
@bot.message_handler(commands=["start"])
def send_welcome_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('/groupe')
    markup.add(button)
    bot.send_message(message.chat.id, "welcome to the my bot💩", reply_markup=markup)


@bot.message_handler(commands=["groupe"])
def send_groupe(message):
    groupes = ''
    for groupe in lessons:
        groupes += f'{groupe}\n'
    bot.send_message(message.chat.id, groupes)

@bot.message_handler(content_types=['text'])
def listener(message):
    if message.chat.type == 'private': 
        try:
            groupeLessons = lessons[message.text]
            with open('choiseGroupe.json', 'w') as file:
                json.dump({"groupe": message.text}, file)
            days = ''
            for day in groupeLessons:
                days += f'{day}\n'
            bot.send_message(message.chat.id, days)
        except KeyError:
            pass
        try:
            with open('choiseGroupe.json', 'r') as file:
                choiseGroupe = json.load(file)
            day = lessons[choiseGroupe['groupe']][message.text]
            dayLessons = ''
            for lessonNumber in day:
                dayLessons += f'{lessonNumber}. {day[lessonNumber]["name"]} {day[lessonNumber]["time"]}\n'
            bot.send_message(message.chat.id, dayLessons) 
        except KeyError:
            pass
        
bot.polling()
