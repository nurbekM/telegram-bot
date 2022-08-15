import telebot
from telebot import types
from lowprice import low_price_parsing

bot = telebot.TeleBot('5327781257:AAGFWr9V4XqtXAVSakiSppTBdAESTTrjMJ0')
command = ''
city_name = ''
number_of_hotels = 0
number_of_photo = 0


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    low_price = types.KeyboardButton('Cheap hotels')
    high_price = types.KeyboardButton('Expensive hotels')
    best_deal = types.KeyboardButton('Best deal')
    history = types.KeyboardButton('Search history')
    markup.add(low_price, high_price, best_deal, history)

    mess = f'Здравствуйте, <b>{message.from_user.first_name}</b>. ' \
           f'Вас, приветствует бот турагентство "Too Easy Travel"   '
    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def messages_replay(message):
    global command
    if message.text == 'Cheap hotels':
        command = 'PRICE_LOWEST_FIRST'
        bot.send_message(message.chat.id, 'Enter the city where the search will be located')
        bot.register_next_step_handler(message, get_city_name)


def get_city_name(message):
    global city_name
    city_name = message.text

    bot.send_message(message.chat.id, 'How many hotels to display, max=25')
    bot.register_next_step_handler(message, get_number_of_hotels)


def get_number_of_hotels(message):
    global number_of_hotels
    number_of_hotels = message.text

    markup = types.InlineKeyboardMarkup(row_width=2)
    button_one = types.InlineKeyboardButton(text='Yes', callback_data='yes')
    button_two = types.InlineKeyboardButton(text='No', callback_data='no')
    markup.add(button_one, button_two)
    bot.send_message(message.chat.id, 'Looking for hotel photos?', parse_mode='html', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global city_name, number_of_hotels, number_of_photo, command

    if call.data == "yes":
        photo = True
        result = low_price_parsing(city_name, number_of_hotels, number_of_photo, photo, command)
        for element in result:
            bot.send_message(call.from_user.id, element)

    elif call.data == "no":
        photo = False
        result = low_price_parsing(city_name, number_of_hotels, number_of_photo, photo,  command)
        for element in result:
            bot.send_message(call.from_user.id, element)


bot.polling(none_stop=True, interval=0)
