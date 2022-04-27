import datetime
import json
import string

from aiogram import Dispatcher, types


# @dp.message_handler()
async def message_filter(message:types.Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')}\
        .intersection(set(json.load(open('cenz.json')))) != set():
        await message.reply('Не говори так! Я слежу за тобой.')
        await message.delete()
        nowdatetime = datetime.datetime.now()
        now = nowdatetime.strftime('[%d/%m/%Y %H:%M:%S]')
        print(now, message.from_user.first_name + ' ругнулся cenz')
    if 'пизд' in message.text.lower():
        try:
            await message.reply('Не говори так! Я слежу за тобой.')
            await message.delete()
            print(now, message.from_user.first_name + ' ругнулся')
        except:
            print(now, message.from_user.first_name + ' ругнулся except')
    if 'залуп' in message.text.lower():
        try:
            await message.reply('Не говори так! Я слежу за тобой.')
            await message.delete()
            print(now, message.from_user.first_name + ' ругнулся')
        except:
            print(now, message.from_user.first_name + ' ругнулся except')
    if 'хуй' in message.text.lower():
        try:
            await message.reply('Не говори так! Я слежу за тобой.')
            await message.delete()
            print(now, message.from_user.first_name + ' ругнулся')
        except:
            print(now, message.from_user.first_name + ' ругнулся except')
    if 'уеба' in message.text.lower():
        try:
            await message.reply('Не говори так! Я слежу за тобой.')
            await message.delete()
            print(now, message.from_user.first_name + ' ругнулся')
        except:
            print(now, message.from_user.first_name + ' ругнулся except')
    if 'пидор' in message.text.lower():
        try:
            await message.reply('Не говори так! Я слежу за тобой.')
            await message.delete()
            print(now, message.from_user.first_name + ' ругнулся')
        except:
            print(now, message.from_user.first_name + ' ругнулся except')
    if 'хуесос' in message.text.lower():
        try:
            await message.reply('Не говори так! Я слежу за тобой.')
            await message.delete()
            print(now, message.from_user.first_name + ' ругнулся')
        except:
            print(now, message.from_user.first_name + ' ругнулся except')


def register_handlers_other(dp:Dispatcher):
    dp.register_message_handler(message_filter)
