from cgitb import text

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.utils.markdown import bold

from config import TOKEN


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Здравствуй пользователь, я твой личный помощник в этом мире!\nИспользуй /info, "
                        "чтобы узнать список доступных команд!")


@dp.message_handler(commands=['info'])
async def process_info_command(message: types.Message):
    await message.reply("Сейчас я могу ответить только на эти команды!\n /profile, /newprofile, /locate ")


@dp.message_handler(commands=['profile'])
async def process_profile_command(message: types.Message):
    await message.reply('У тебя нет профиля!)')


@dp.message_handler(commands=['newprofile'])
async def process_newprofile_commnad(message: types.Message):
    await message.reply('Прости, пока что ты не можешь создать профиль ;(((')



@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)


if __name__ == '__main__':
    executor.start_polling(dp)