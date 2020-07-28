import telebot
import environ
from telebot import types

from html_parser import serials, get_episode_info, get_serial_html_info

environ.Env.read_env()
env = environ.Env()
TOKEN = env('TELEGRAM_TOKEN')

bot = telebot.TeleBot(TOKEN)
keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row('Поиск', 'Конец', 'Ясно!!!')


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start', reply_markup=keyboard1)


@bot.message_handler(commands=['show'])
def show_command(message):
    keyboard = types.InlineKeyboardMarkup()
    for serial_name, _ in serials.items():
        btn_my_site = types.InlineKeyboardButton(text=serial_name, callback_data=serial_name)
        keyboard.add(btn_my_site)
    bot.send_message(message.chat.id, "Список сериалов:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call: types.CallbackQuery):
    if call.message:
        serial_url = serials[call.data]
        serial_info = get_episode_info(get_serial_html_info(serial_url))
        bot.send_message(call.message.chat.id, f'Для сериала "{call.data}", {serial_info}')


wait_messages = {}


@bot.message_handler(content_types=['text'])
def receive_message(message: types.Message):
    if wait_messages.get(message.chat.id) or False:
        keyboard = types.InlineKeyboardMarkup()
        for serial_name, serial_url in serials.items():
            if serial_name.startswith(message.text):
                btn_my_site = types.InlineKeyboardButton(text=serial_name, callback_data=serial_name)
                keyboard.add(btn_my_site)

        bot.send_message(message.chat.id, 'По вашему запросу были найдены: ', reply_markup=keyboard)
        wait_messages[message.chat.id] = False

    if message.text.lower() == 'поиск':
        wait_messages[message.chat.id] = True
        bot.send_message(message.chat.id, 'Введите название сериала:')
    elif message.text.lower() == 'конец':
        #  Открытие аудио
        with open('/home/felix/PycharmProjects/Wecreateterribles/good_job.mp3', 'rb') as _file:
            audio = _file.read()
        # Отправка
        bot.send_audio(message.chat.id, audio=audio)
    elif message.text == 'ясно!!!':  # Кнопка 'ясно!!!' должна отправлять стикер
        sticker = 'CAACAgIAAxkBAAMhXrEiC5rUiGT-ceiKkmiwjJou1xIAAg8DAAJtsEIDDrRMZLudXUYZBA'
        bot.send_sticker(message.chat.id, sticker)


if __name__ == '__main__':
    bot.polling()
