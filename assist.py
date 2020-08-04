import os
from typing import Union

import environ
from telebot import types, TeleBot

from html_parser import serials, get_episode_info, get_serial_html_info
from periodic_tasks import add_task

environ.Env.read_env()
env = environ.Env()
TOKEN = env('TELEGRAM_TOKEN')
BASE = os.path.dirname(__file__)

bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_command(message: types.Message):
    main_keyboard = types.ReplyKeyboardMarkup()
    main_keyboard.row('Поиск', 'Конец',)
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start', reply_markup=main_keyboard)


@bot.message_handler(commands=['show'])
def show_command(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    for serial_id, serial in serials.items():  # type: int, dict
        keyboard.add(types.InlineKeyboardButton(text=serial['name'], callback_data=f'serial:{serial_id}'))
    bot.send_message(message.chat.id, "Список сериалов которые выходят на данный момент:", reply_markup=keyboard)


# @bot.message_handler(commands=['test'])
# def show_command(message: types.Message):
#     keyboard = types.InlineKeyboardMarkup()
# for f in ['Хорошо', 'Плохо']:
#     keyboard.add(types.InlineKeyboardButton(text=f, callback_data=f'{f}'))
# bot.send_message(message.chat.id, 'Как дела?', reply_markup=keyboard)


time_notify = {
        1: 'За час до выхода',
        2: 'За пол часа до выхода',
    }


def add_notification(call, serial_id):
    keyboard = types.InlineKeyboardMarkup()
    for time in time_notify:
        keyboard.add(types.InlineKeyboardButton(text=time_notify[time],
                                                callback_data=f'create_notification:{serial_id}',
                                                ))
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        text=f'Оповестить за: ',
        message_id=call.message.message_id,
        reply_markup=keyboard,
    )


def get_serial_info(call, serial_id):
    serial = serials[serial_id]
    serial_info = get_episode_info(get_serial_html_info(serial['url']))
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(
        text='Создать оповещение',
        callback_data=f'add_notification:{call.data}',
    ))
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        text=f'Для сериала "{serial["name"]}", {serial_info}',
        message_id=call.message.message_id,
        reply_markup=keyboard,
    )


def create_notification(call, serial_id):
    serial = serials[serial_id]
    add_task(serial['url'], call.message)
    bot.answer_callback_query(call.id, text="Оповещение создано!")
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Изменить оповещение', callback_data=f'edit_notification:{serial_id}'))
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        text=serial['name'],
        message_id=call.message.message_id,
        reply_markup=keyboard,
    )


def completion_of_changes(call, serial_id):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(
        text='Конец!',
        callback_data=f'notify_end:{serial_id}',
    ))
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        text=f'Оповещение изменено!',
        message_id=call.message.message_id,
        reply_markup=keyboard,
    )


callbacks = {
    'add_notification': add_notification,
    'edit_notification': add_notification,
    'serial': get_serial_info,
    'create_notification': create_notification,
    'completion_of_changes': completion_of_changes,
}


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call: types.CallbackQuery):
    if call.message:
        call_back_params = call.data.split(':')
        print(call_back_params)
        call_back_key = call_back_params[0]
        call_back_func = callbacks[call_back_key]
        call_back_func(call, int(call_back_params[-1]))


wait_messages = {}


def find_serials(search_text: str) -> Union[types.InlineKeyboardMarkup, None]:
    keyboard = types.InlineKeyboardMarkup()
    for serial_id, serial in serials.items():
        # if search_text.lower() in serial_name.lower():
        if serial['name'].lower().startswith(search_text.lower()):
            keyboard.add(types.InlineKeyboardButton(text=serial['name'], callback_data=f'serial:{serial_id}'))
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
