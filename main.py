from telebot import *
import config
from text_const import buttons, messages
from game_functions import *
import random
from my_functions import create_reply_keyboard, send_url_photo, send_file_photo, create_inline_keyboard
import sqlite3

sqlite_connect = sqlite3.connect('players.db', check_same_thread=False)
sqlite_create_table = 'CREATE TABLE IF NOT EXISTS players (id INTEGER PRIMARY KEY, telegram_id INTEGER UNIQUE,' \
                      ' name TEXT, choice TEXT, message TEXT, buttons TEXT)'
cursor = sqlite_connect.cursor()
cursor.execute(sqlite_create_table)
cursor.close()

bot = telebot.TeleBot(config.TG_TOKEN)


def create_game_field(message):
    butt = messages.STAR + messages.STAR + messages.STAR + messages.STAR + messages.STAR \
           + messages.STAR + messages.STAR + messages.STAR + messages.STAR
    sql_insert_query = f'UPDATE players SET buttons = "{butt}" WHERE telegram_id = "{message.from_user.id}"'
    cur = sqlite_connect.cursor()
    try:
        cur.execute(sql_insert_query)
    except TypeError:
        player_to_database(message)
        cur.execute(sql_insert_query)
    sqlite_connect.commit()
    cur.close()


def player_to_database(message):
    last_name = message.from_user.last_name
    if last_name is None:
        name = message.from_user.first_name
    else:
        name = message.from_user.first_name + message.from_user.last_name
    sql_insert_query = f'INSERT OR IGNORE INTO players(telegram_id, name, message, choice)' \
                       f' VALUES("{message.from_user.id}", "{name}", " ", " ")'
    cur = sqlite_connect.cursor()
    cur.execute(sql_insert_query)
    sqlite_connect.commit()
    cur.close()
    create_game_field(message)


def update_choice(message):
    sql_insert_query = f'UPDATE players SET choice = "{message.text}" WHERE telegram_id = "{message.from_user.id}"'
    cur = sqlite_connect.cursor()

    cur.execute(sql_insert_query)
    '''except:
        player_to_database(message)
        cur.execute(sql_insert_query)'''
    sqlite_connect.commit()
    cur.close()


def return_from_callback(callback):
    cur = sqlite_connect.cursor()
    try:
        res = cur.execute(f'SELECT buttons FROM players WHERE telegram_id = "{callback.from_user.id}"')
        butt = res.fetchone()[0]
        res = cur.execute(f'SELECT choice FROM players WHERE telegram_id = "{callback.from_user.id}"')
        choice = res.fetchone()[0]
        res = cur.execute(f'SELECT message FROM players WHERE telegram_id = "{callback.from_user.id}"')
        mess = res.fetchone()[0]
        res = cur.execute(f'SELECT name FROM players WHERE telegram_id = "{callback.from_user.id}"')
        name = res.fetchone()[0]
    except TypeError:
        player_to_database(callback)
        res = cur.execute(f'SELECT buttons FROM players WHERE telegram_id = "{callback.from_user.id}"')
        butt = res.fetchone()[0]
        res = cur.execute(f'SELECT choice FROM players WHERE telegram_id = "{callback.from_user.id}"')
        choice = res.fetchone()[0]
        res = cur.execute(f'SELECT message FROM players WHERE telegram_id = "{callback.from_user.id}"')
        mess = res.fetchone()[0]
        res = cur.execute(f'SELECT name FROM players WHERE telegram_id = "{callback.from_user.id}"')
        name = res.fetchone()[0]
    cur.close()
    return butt, choice, mess, name


def update_database(message, butt, mess):
    sql_insert_query = f'UPDATE players SET buttons = "{butt}", message = "{mess}"' \
                       f' WHERE telegram_id = "{message.from_user.id}"'
    cur = sqlite_connect.cursor()
    try:
        cur.execute(sql_insert_query)
    except TypeError:
        player_to_database(message)
        cur.execute(sql_insert_query)
    sqlite_connect.commit()
    cur.close()


@bot.inline_handler(func=lambda query: 'кот' in query.query or 'cat' in query.query)
def query_photo(inline_query):
    send_url_photo(bot, inline_query)


@bot.message_handler(commands=['start'])
def start(message):
    player_to_database(message)
    cur = sqlite_connect.cursor()
    message_id = message.chat.id
    user_id = message.from_user.id
    res = cur.execute(f'SELECT name FROM players WHERE telegram_id="{user_id}"')
    name = res.fetchone()[0]
    cur.close()
    markup = create_reply_keyboard()
    send_message = f'Привет, <b>{name}</b>'
    bot.send_message(message_id, send_message, parse_mode='html', reply_markup=markup)


@bot.message_handler()
def bot_message(message):
    message_id = message.chat.id
    if message.text == buttons.HELP_BUTTON or message.text == '/help' or message.text == '/help@ghauruXO_bot' \
            or 'помощь' in message.text.lower():
        send_message = messages.HELP
        bot.send_message(message_id, send_message, parse_mode='html')
    if message.text == buttons.PLAY_BUTTON or message.text == '/play' or message.text == '/play@ghauruXO_bot' \
            or 'игра' in message.text.lower():
        create_game_field(message)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        first_button = types.KeyboardButton(messages.X)
        second_button = types.KeyboardButton(messages.O)
        markup.add(first_button, second_button)
        bot.send_message(message_id, messages.SIDE_CHOICE, reply_markup=markup)
    if message.text == messages.X or message.text == messages.O:
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message_id, 'Начинается игра...', reply_markup=markup)
        update_choice(message)
        markup = create_inline_keyboard()
        bot.send_message(message_id, 'Выберите кнопку', reply_markup=markup)
    if message.text == '/cat' or message.text == buttons.CAT_BUTTON or message.text == '/cat@ghauruXO_bot' \
            or 'кот' in message.text.lower():
        send_file_photo(bot, message_id)
    if 'скрыть' in message.text.lower() or message.text == '/remove':
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message_id, 'Скрываю меню бота', reply_markup=markup)
    if message.text.lower() == 'меню' or message.text.lower() == 'menu' or message.text.lower() == '/menu' \
            or message.text == '/menu@ghauruXO_bot':
        markup = create_reply_keyboard()
        bot.send_message(message_id, 'Меню бота', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: callback.data)
def change_callback_buttons(callback):
    butt, choice, mess, name = return_from_callback(callback)
    message_id = callback.message.chat.id
    if check_victory(butt) or check_tie(butt):
        win = who_won(butt, choice)
        if win != 'D':
            if choice == win:
                mess = f'Игрок <b>{name}</b> уже выйграл'
            else:
                mess = 'Бот уже выйграл'
        else:
            mess = f'Уже ничья между <b>{name}</b> и ботом'
        bot.send_message(message_id, mess, parse_mode='html')
    else:
        button_list = []
        markup = types.InlineKeyboardMarkup()
        for i in range(1, 10):
            if callback.data == 'btn' + str(i) and butt[i - 1] == messages.STAR:
                butt = butt[:i-1] + choice + butt[i:]
                numbers = []
                mess = 'Выбирайте кнопку'
                for k in range(len(butt)):
                    if butt[k] == messages.STAR:
                        numbers.append(k)
                if choice == messages.X and numbers:
                    bot_turn = random.choice(numbers)
                    if bot_turn != 8:
                        butt = butt[:bot_turn] + messages.O + butt[bot_turn + 1:]
                    else:
                        butt = butt[:bot_turn] + messages.O
                elif numbers:
                    bot_turn = random.choice(numbers)
                    if bot_turn != 8:
                        butt = butt[:bot_turn] + messages.X + butt[bot_turn + 1:]
                    else:
                        butt = butt[:bot_turn] + messages.X
            elif callback.data == 'btn' + str(i) and butt[i - 1] != messages.STAR:
                if mess == messages.TAKEN_SPOT:
                    mess = messages.TAKEN_SPOT2
                else:
                    mess = messages.TAKEN_SPOT
        for i in range(1, 10):
            button = types.InlineKeyboardButton(butt[i - 1], callback_data='btn' + str(i))
            button_list.append(button)
        markup.add(button_list[0], button_list[1], button_list[2], button_list[3], button_list[4],
                   button_list[5], button_list[6], button_list[7], button_list[8])
        if check_victory(butt) or check_tie(butt):
            win = who_won(butt, choice)
            if win != 'D':
                if choice == who_won(butt, choice):
                    mess = f'Игрок <b>{name}</b> выйграл'
                    bot.send_message(chat_id=message_id, text='Молодец, держи котика за победу!')
                    send_file_photo(bot, message_id)
                else:
                    mess = 'Бот выйграл'
            else:
                mess = f'Ничья между <b>{name}</b> и ботом'
        bot.edit_message_text(chat_id=message_id, message_id=callback.message.id,
                              text=mess, reply_markup=markup, parse_mode='html')
    update_database(callback, butt, mess)


bot.polling(none_stop=True)
