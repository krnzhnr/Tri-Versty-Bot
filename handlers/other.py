import json, string
from aiogram import types, Dispatcher
from create_bot import dp


# Фильтр мата
# @dp.message_handler()
async def message_filter(message:types.Message):
    # try:
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')}\
        .intersection(set(json.load(open('cenz.json')))) != set():
        await message.reply('Не говори так! Я слежу за тобой.')
        await message.delete()
    # except:
    if 'пизд' in message.text.lower():
        await message.reply('Не говори так! Я слежу за тобой.')
        await message.delete()
    if 'залуп' in message.text.lower():
        await message.reply('Не говори так! Я слежу за тобой.')
        await message.delete()
    if 'хуй' in message.text.lower():
        await message.reply('Не говори так! Я слежу за тобой.')
        await message.delete()
    if 'уеба' in message.text.lower():
        await message.reply('Не говори так! Я слежу за тобой.')
        await message.delete()
    if 'пидор' in message.text.lower():
        await message.reply('Не говори так! Я слежу за тобой.')
        await message.delete()
    if 'хуесос' in message.text.lower():
        await message.reply('Не говори так! Я слежу за тобой.')
        await message.delete()


# Регистрация хендлера
def register_handlers_other(dp:Dispatcher):
    dp.register_message_handler(message_filter)
