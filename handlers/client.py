import datetime

from aiogram import Dispatcher, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from create_bot import bot
from data_base import sqlite_announcements_db, sqlite_users_db

admin_button = KeyboardButton('/moderator')
start_button = KeyboardButton('/start')

help_button = KeyboardButton('/Помощь')
vk_button = KeyboardButton('/ВК')
weather_button = KeyboardButton('/Погода')
announcements_button = KeyboardButton('/Анонсы')
help_kb = ReplyKeyboardMarkup(resize_keyboard=True).\
    row(announcements_button, weather_button, vk_button).\
    row(help_button)


# @dp.message_handler(commands=['start'])
async def start(message: types.Message):
    nowdatetime = datetime.datetime.now()
    now = nowdatetime.strftime('[%d/%m/%Y %H:%M:%S]')
    try:
        # await message.delete()
        userdata = {}
        userdata = {'id':message.from_user.id, 
                    'username':message.from_user.username, 
                    'first_name':message.from_user.first_name}
        print(userdata)
        if await sqlite_users_db.sql_add_user(userdata) is True:
            await bot.send_message(message.from_user.id, 
                                   'Привет, 'f" {userdata['first_name']}, "' я тебя помню!', 
                                   reply_markup=help_kb)
            nowdatetime = datetime.datetime.now()
            now = nowdatetime.strftime('[%d/%m/%Y %H:%M:%S]')
            print(now, f'{message.from_user.first_name} вернулся!')
        else:
            await bot.send_message(message.from_user.id, 'Привет! Я буду следить за порядком в чате Три Версты \
и предоставлять полезную информацию!\nДля управления ботом используй кнопки.', reply_markup=help_kb)
    except Exception as exc:
        await message.answer('Чтобы использовать бота напиши ему в ЛС:\n@penis_mudilaBot', reply_markup=help_kb)
        await message.delete()
        print(now, exc)


# @dp.message_handler(commands=['Анонсы'])
async def announcements(message: types.Message):
    nowdatetime = datetime.datetime.now()
    now = nowdatetime.strftime('[%d/%m/%Y %H:%M:%S]')
    try:
        print(now, message.from_user.first_name + ' запросил анонсы')
        await sqlite_announcements_db.sql_read(message)
        await message.delete()
    except Exception as exc:
        await message.answer('Общение с ботом через ЛС, напиши ему:\n@penis_mudilaBot')
        await message.delete()
        print(now, exc)


# @dp.message_handler(commands=['help'])
async def help(message: types.Message):
    nowdatetime = datetime.datetime.now()
    now = nowdatetime.strftime('[%d/%m/%Y %H:%M:%S]')
    try:
        await bot.send_message(message.from_user.id, """
    Вот список моих команд:

/Анонсы - бот отправляет вам в ЛС все актуальные на данный момент анонсы

/ВК - Наша группа ВК со всеми фотографиями

/Погода - Текущая погода и прогноз

/Помощь - Помощь по командам
""", reply_markup=help_kb)
        await message.delete()
        print(now, message.from_user.first_name + ' запросил помощь')
    except Exception as exc:
        await message.answer('Общение с ботом через ЛС, напиши ему:\n@penis_mudilaBot')
        await message.delete()
        print(now, exc)


# @dp.message_handler(commands=['vk'])
async def vk_group(message: types.Message):
    nowdatetime = datetime.datetime.now()
    now = nowdatetime.strftime('[%d/%m/%Y %H:%M:%S]')
    try:
        await bot.send_message(message.from_user.id, """Наша группа ВК с фоточками:
https://vk.com/kubok_tri_versty
""", reply_markup=(help_kb))
        await message.delete()
        print(now, message.from_user.first_name + ' запросил ВК')
    except Exception as exc:
        await message.answer('Общение с ботом через ЛС, напиши ему:\n@penis_mudilaBot')
        await message.delete()
        print(now, exc)


# @dp.message_handler(content_types=['new_chat_members'])
async def user_joined(message: types.Message):
    nowdatetime = datetime.datetime.now()
    now = nowdatetime.strftime('[%d/%m/%Y %H:%M:%S]')
    await message.answer(message.from_user.first_name + ', добро пожаловать в чат!\n\
Я буду следить за порядком в чате Три Версты \
и предоставлять полезную информацию!\n\
Чтобы увидеть список моих команд нажми кнопку /Помощь', reply_markup=help_kb)
    print(now, message.from_user.first_name + ' вошел в чат')


# @dp.message_handler(content_types=['left_chat_member'])
async def user_left(message: types.Message):
    nowdatetime = datetime.datetime.now()
    now = nowdatetime.strftime('[%d/%m/%Y %H:%M:%S]')
    await message.answer(message.from_user.first_name + ', мы будем по тебе скучать!')
    try:
        await bot.send_message(message.from_user.first_name + ', мы будем по тебе скучать!')
    except:
        print(now, message.from_user.first_name + ' не получил прощание в ЛС')
    print(now, message.from_user.first_name + ' покинул чат')
    

def register_handlers_client(dp:Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(announcements, commands=['Анонсы'])
    dp.register_message_handler(help, commands=['Помощь'])
    dp.register_message_handler(vk_group, commands=['ВК'])
    dp.register_message_handler(user_joined, content_types=['new_chat_members'])
    dp.register_message_handler(user_left, content_types=['left_chat_member'])
