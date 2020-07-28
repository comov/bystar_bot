import os
from typing import Union

import environ
from telebot import types, TeleBot

from html_parser import serials, get_episode_info, get_serial_html_info

environ.Env.read_env()
env = environ.Env()
TOKEN = env('TELEGRAM_TOKEN')
BASE = os.path.dirname(__file__)

bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_command(message: types.Message):
    main_keyboard = types.ReplyKeyboardMarkup()
    main_keyboard.row('Поиск', 'Конец')
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start', reply_markup=main_keyboard)


@bot.message_handler(commands=['show'])
def show_command(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    for serial_name, _ in serials.items():  # type: str
        keyboard.add(types.InlineKeyboardButton(text=serial_name, callback_data=serial_name))
    bot.send_message(message.chat.id, "Список сериалов:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call: types.CallbackQuery):
    if call.message:
        serial_info = get_episode_info(get_serial_html_info(serials[call.data]))
        bot.send_message(call.message.chat.id, f'Для сериала "{call.data}", {serial_info}')


wait_messages = {}


def find_serials(search_text: str) -> Union[types.InlineKeyboardMarkup, None]:
    keyboard = types.InlineKeyboardMarkup()
    for serial_name, _ in serials.items():
        # if search_text.lower() in serial_name.lower():
        if serial_name.lower().startswith(search_text.lower()):
            keyboard.add(types.InlineKeyboardButton(text=serial_name, callback_data=serial_name))
    return keyboard if keyboard.keyboard else None


@bot.message_handler(content_types=['text'])
def receive_message(message: types.Message):
    if wait_messages.get(message.chat.id) or False:
        keyboard = find_serials(message.text)
        message_text = 'По вашему запросу были найдены:' if keyboard else 'По вашему ничего не найдено :('
        bot.send_message(message.chat.id, message_text, reply_markup=keyboard)
        wait_messages[message.chat.id] = False

    if message.text.lower() == 'поиск':
        wait_messages[message.chat.id] = True
        bot.send_message(message.chat.id, 'Введите название сериала:')
    elif message.text.lower() == 'конец':
        #  Открытие аудио
        with open(f'{BASE}/good_job.mp3', 'rb') as _file:
            audio = _file.read()
        # Отправка
        bot.send_audio(message.chat.id, audio=audio)


if __name__ == '__main__':
    bot.polling()
