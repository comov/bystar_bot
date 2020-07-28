import telebot
import environ

environ.Env.read_env()
env = environ.Env()
TOKEN = env('TELEGRAM_TOKEN')

bot = telebot.TeleBot(TOKEN)
keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row('привет', 'пока', 'чё как?', 'конец', 'ясно!!!')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start', reply_markup=keyboard1)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет, мой создатель')
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Прощай, создатель')
    elif message.text.lower() == 'чё как?':
        bot.send_message(message.chat.id, 'Намана, ты сам как?')
    elif message.text.lower() == 'конец':
        #  Открытие аудио
        with open('/home/felix/PycharmProjects/Wecreateterribles/good_job.mp3', 'rb') as _file:
            audio = _file.read()
        # Отправка
        bot.send_audio(message.chat.id, audio=audio)
    elif message.text == 'ясно!!!':  # Кнопка 'ясно!!!' должна отправлять стикер
        sticker = 'CAACAgIAAxkBAAMhXrEiC5rUiGT-ceiKkmiwjJou1xIAAg8DAAJtsEIDDrRMZLudXUYZBA'
        bot.send_sticker(message.chat.id, sticker)


bot.polling()
