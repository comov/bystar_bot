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
    main_keyboard.row('Поиск', 'Конец', 'Посмотреть список всех сериалов много через комнаду /show')
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start', reply_markup=main_keyboard)


@bot.message_handler(commands=['show'])
def show_command(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    for serial_name, _ in serials.items():  # type: str
        keyboard.add(types.InlineKeyboardButton(text=serial_name, callback_data=f'serial:{serial_name}'))
    bot.send_message(message.chat.id, "Список сериалов:", reply_markup=keyboard)


# @bot.message_handler(commands=['test'])
# def show_command(message: types.Message):
#     keyboard = types.InlineKeyboardMarkup()
# for f in ['Хорошо', 'Плохо']:
#     keyboard.add(types.InlineKeyboardButton(text=f, callback_data=f'{f}'))
# bot.send_message(message.chat.id, 'Как дела?', reply_markup=keyboard)

serials_id = {
    'Боруто: Новое поколение Наруто': 1,
    'Мастера Меча': 2,
}
serials_id_revert = {
    1: 'Боруто: Новое поколение Наруто',
    2: 'Мастера Меча',
}


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call: types.CallbackQuery):
    if call.message:
        link = serials.get(call.data)
        # if call.data == 'Хорошо':
        #     bot.send_message(call.message.chat.id, 'Вот и хорошо')
        # if call.data == 'Плохо':
        #     bot.send_message(call.message.chat.id, 'Сочувствую')
        if link:
            serial_info = get_episode_info(get_serial_html_info(link))
            keyboard = types.InlineKeyboardMarkup()
            serial_id = serials_id[call.data]
            keyboard.add(types.InlineKeyboardButton(text='Создать оповещение',
                                                    callback_data=f'add_notification:{serial_id}',
                                                    ))
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                text=f'Для сериала "{call.data}", {serial_info}',
                message_id=call.message.message_id,
                reply_markup=keyboard,
            )
        elif call.data == 'add_notification:1' or call.data == 'add_notification:2':
            serial_id = int(call.data[-1])
            keyboard = types.InlineKeyboardMarkup()
            for i in ['За час до выхода', 'За пол часа до выхода']:
                keyboard.add(types.InlineKeyboardButton(text=i, callback_data=f'notify:{serial_id}'))
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                text=f'Оповестить за: ',
                message_id=call.message.message_id,
                reply_markup=keyboard,
            )
        elif call.data == 'notify:1' or call.data == 'notify:2':
            add_task(link, call.message)
            bot.answer_callback_query(call.id, text="Оповещение создано!")
            serial_id = int(call.data[-1])
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text='Изменить оповещение', callback_data=f'notify:{serial_id}'))
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                text=serials_id_revert[serial_id],
                message_id=call.message.message_id,
                reply_markup=keyboard,
            )


wait_messages = {}


def find_serials(search_text: str) -> Union[types.InlineKeyboardMarkup, None]:
    keyboard = types.InlineKeyboardMarkup()
    for serial_name, _ in serials.items():
        # if search_text.lower() in serial_name.lower():
        if serial_name.lower().startswith(search_text.lower()):
            keyboard.add(types.InlineKeyboardButton(text=serial_name, callback_data=f'{serial_name}'))
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
    elif message.text.lower() == 'посмотреть список всех сериалов много через комнаду /show':
        bot.send_sticker(message.chat.id, 'CAACAgUAAxkBAAEBHZBfIVhyCG9qxYcczZSbaYgTeo59NwACtBoAAsZRxhU9mBXY6JGNpxoE')


if __name__ == '__main__':
    bot.polling()
