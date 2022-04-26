import telebot
from anekdot import list_of_jokes
from config import TOKEN
from mg import get_map_cell

bot = telebot.TeleBot(TOKEN)
cols, rows = 8, 8

keyboard = telebot.types.InlineKeyboardMarkup()
keyboard.row( telebot.types.InlineKeyboardButton('←', callback_data='left'),
			  telebot.types.InlineKeyboardButton('↑', callback_data='up'),
			  telebot.types.InlineKeyboardButton('↓', callback_data='down'),
			  telebot.types.InlineKeyboardButton('→', callback_data='right') )

keyboard2 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
td = telebot.types.KeyboardButton("Maze")
back = telebot.types.KeyboardButton("Back")
keyboard2.add(td, back)

markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
tank_game = telebot.types.KeyboardButton("Tank Game")
maze_game = telebot.types.KeyboardButton("Maze Game")
help = telebot.types.KeyboardButton("Help")
anekdot = telebot.types.KeyboardButton("Anekdot")

markup.add(tank_game, maze_game, help, anekdot)

maps = {}

@bot.message_handler(commands=['start'])
def start(message):
    sti = open('static/AnimatedSticker7.tgs', 'rb')
    bot.send_sticker(message.chat.id, sti)

    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b> {1.first_name} </b>, игровой бот.".format(message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)

def get_map_str(map_cell, player):
    map_str = ""
    for y in range(rows * 2 - 1):
        for x in range(cols * 2 - 1):
            if map_cell[x + y * (cols * 2 - 1)]:
                map_str += "⬛"
            elif (x, y) == player:
                map_str += "🔴"
            else:
                map_str += "⬜"
        map_str += "\n"

    return map_str

@bot.message_handler(content_types=['text'])
def play_maze(message):
    map_cell = get_map_cell(cols, rows)

    user_data = {
        'map': map_cell,
        'x': 0,
        'y': 0
    }

    maps[message.chat.id] = user_data

    if message.chat.type == 'private':
        if message.text == 'Maze Game':
            bot.send_message(message.from_user.id, get_map_str(map_cell, (0, 0)), reply_markup=keyboard)
        elif message.text == 'Help':
            bot.send_message(message.chat.id, 'Это помощь', reply_markup=keyboard2)
        elif message.text == 'Anekdot':
            bot.send_message(message.chat.id, 'Здравствуйте! Чтобы посмеяться введите любую цифру:')
        elif message.text == 'Maze':
            bot.send_message(message.chat.id, 'fefsrgergr')

    if message.text.lower() in '123456789':
        bot.send_message(message.chat.id, list_of_jokes[0])
        del list_of_jokes[0]

@bot.callback_query_handler(func=lambda call: True)
def callback_func(query):
    user_data = maps[query.message.chat.id]
    new_x, new_y = user_data['x'], user_data['y']

    if query.data == 'left':
        new_x -= 1
    if query.data == 'right':
        new_x += 1
    if query.data == 'up':
        new_y -= 1
    if query.data == 'down':
        new_y += 1

    if new_x < 0 or new_x > 2 * cols - 2 or new_y < 0 or new_y > rows * 2 - 2:
        return None
    if user_data['map'][new_x + new_y * (cols * 2 - 1)]:
        return None

    user_data['x'], user_data['y'] = new_x, new_y

    if new_x == cols * 2 - 2 and new_y == rows * 2 - 2:
        bot.edit_message_text( chat_id=query.message.chat.id,
                               message_id=query.message.id,
                               text="Вы выиграли" )
        return None

    bot.edit_message_text(chat_id=query.message.chat.id,
                            message_id=query.message.id,
                            text=get_map_str(user_data['map'], (new_x, new_y)),
                            reply_markup=keyboard)


bot.polling(none_stop=True, interval=0)
