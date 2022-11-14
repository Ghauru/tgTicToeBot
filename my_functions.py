from telebot import types
from text_const import buttons, messages
from requests import get
import random


def create_reply_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button1 = types.KeyboardButton(buttons.PLAY_BUTTON)
    button2 = types.KeyboardButton(buttons.HELP_BUTTON)
    button3 = types.KeyboardButton(buttons.CAT_BUTTON)
    button4 = types.KeyboardButton(buttons.REMOVE_MENU)
    markup.add(button1, button2, button3, button4)
    return markup


def send_url_photo(bot, inline_query):
    try:
        k = 1
        temp = ''
        photo_list = []
        while k < 5:
            source = get(f"https://aws.random.cat/view/{random.choice(range(1000))}").text
            if source != temp:
                photo = source.split("src=\"")[1].split("\"")[0]
                temp = photo
                r = types.InlineQueryResultPhoto(str(k), photo, photo)
                photo_list.append(r)
                k += 1
        bot.answer_inline_query(inline_query.id, photo_list, cache_time=1)
    except:
        return send_url_photo(bot, inline_query)


def send_file_photo(bot, message_id):
    with open('Cats/' + str(random.choice([i for i in range(601)])) + '.jpg', 'rb') as g:
        if g:
            bot.send_photo(message_id, g)
        else:
            send_file_photo(bot, message_id)


def create_inline_keyboard():
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(messages.STAR, callback_data='btn1')
    button2 = types.InlineKeyboardButton(messages.STAR, callback_data='btn2')
    button3 = types.InlineKeyboardButton(messages.STAR, callback_data='btn3')
    button4 = types.InlineKeyboardButton(messages.STAR, callback_data='btn4')
    button5 = types.InlineKeyboardButton(messages.STAR, callback_data='btn5')
    button6 = types.InlineKeyboardButton(messages.STAR, callback_data='btn6')
    button7 = types.InlineKeyboardButton(messages.STAR, callback_data='btn7')
    button8 = types.InlineKeyboardButton(messages.STAR, callback_data='btn8')
    button9 = types.InlineKeyboardButton(messages.STAR, callback_data='btn9')
    markup.add(button1, button2, button3, button4, button5, button6, button7, button8, button9)
    return markup