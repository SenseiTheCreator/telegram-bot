import telebot
from currency_converter import CurrencyConverter
from telebot import types

bot = telebot.TeleBot('7375839144:AAH6ColS5ZIlNl4KPH5Z-AOUXIHHafFwnMI')
currency = CurrencyConverter()
amount = 0


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привіт козаче, введи суму')
    bot.register_next_step_handler(message, summa)


def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
        if amount > 0:
            markup = types.InlineKeyboardMarkup(row_width=2)
            btn1 = types.InlineKeyboardButton("USD/EUR", callback_data="usd/eur")
            btn2 = types.InlineKeyboardButton("EUR/USD", callback_data="eur/usd")
            btn3 = types.InlineKeyboardButton("USD/GBP", callback_data="usd/gbp")
            btn4 = types.InlineKeyboardButton("Інша валюта", callback_data="else")
            markup.add(btn1, btn2, btn3, btn4)
            bot.send_message(message.chat.id, 'Виберіть пару валют', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Козаче, число має бути більше за 0. Напишіть суму знову")
            bot.register_next_step_handler(message, summa)
    except ValueError:
        bot.send_message(message.chat.id, "Щось зовсім не той формат. Впишіть суму знову")
        bot.register_next_step_handler(message, summa)


@bot.callback_query_handler(func=lambda call: True)
def callback_data(call):
    global amount
    if call.data != 'else':
        try:
            values = call.data.upper().split('/')
            res = currency.convert(amount, values[0], values[1])
            bot.send_message(call.message.chat.id, f"Конвертація: {round(res, 2)}. Можете знову вписати суму")
            bot.register_next_step_handler(call.message, summa)
        except Exception as e:
            bot.send_message(call.message.chat.id, f"Упс, щось пішло не так: {e}")
            bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, "Введіть пару значень через слеш")
        bot.register_next_step_handler(call.message, mycurrency)


def mycurrency(message):
    global amount
    try:
        values = message.text.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f"Конвертація: {round(res, 2)}. Можете знову вписати суму")
        bot.register_next_step_handler(message, summa)
    except Exception as e:
        bot.send_message(message.chat.id, f"Щось не так. Впишіть значення ще раз. Помилка: {e}")
        bot.register_next_step_handler(message, mycurrency)


bot.polling(non_stop=True)
