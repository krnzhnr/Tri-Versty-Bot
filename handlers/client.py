from aiogram import Dispatcher, types
from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup)
from create_bot import bot, dp
from data_base import sqlite_db

admin_button = KeyboardButton('/moderator')

help_button = KeyboardButton('/Помощь')
vk_button = KeyboardButton('/ВК')
weather_button = KeyboardButton('/Погода')
announcements_button = KeyboardButton('/Анонсы')
help_kb = ReplyKeyboardMarkup(resize_keyboard=True)\
    .add(announcements_button)\
    .add(weather_button)\
    .add(vk_button)\
    .add(help_button)\
    .add(admin_button)


# Функция команды старт
# @dp.message_handler(commands=['start'])
async def start(message:types.Message):
    try:
        await message.answer('Привет! Я буду следить за порядком в чате Три Версты \
и предоставлять полезную информацию!\nДля управления ботом используй кнопки.', reply_markup=help_kb, )
        await message.delete()
    except:
        await message.answer('Общение с ботом через ЛС, напиши ему:\n@penis_mudilaBot')           
        await message.delete()


# @dp.message_handler(commands=['Анонсы'])
async def announcements(message:types.Message):
    try:
        await sqlite_db.sql_read(message)
        await message.delete()
        print(message.from_user.first_name + ' запросил анонсы')
    except:
        await message.answer('Общение с ботом через ЛС, напиши ему:\n@penis_mudilaBot')           
        await message.delete()


# Функция команды хелп
# @dp.message_handler(commands=['help'])
async def help(message:types.Message):
    try:
        await bot.send_message(message.from_user.id, """
    Вот список моих команд:

/Анонсы - бот отправляет вам в ЛС все актуальные на данный момент анонсы

/ВК - Наша группа ВК со всеми фотографиями

/Погода - Текущая погода и прогноз

/Помощь - Помощь по командам
""", reply_markup=help_kb)
        await message.delete()
        print(message.from_user.first_name + ' запросил помощь')
    except:
        await message.answer('Общение с ботом через ЛС, напиши ему:\n@penis_mudilaBot')           
        await message.delete()


# Функция команды вк
# @dp.message_handler(commands=['vk'])
async def vk_group(message:types.Message):
    try:
        await bot.send_message(message.from_user.id, """Наша группа ВК:
https://vk.com/kubok_tri_versty
""", reply_markup=(help_kb))
        await message.delete()
        print(message.from_user.first_name + ' запросил ВК')
    except:
        await message.answer('Общение с ботом через ЛС, напиши ему:\n@penis_mudilaBot')           
        await message.delete()


# Тут по идее будешь встраивать погоду
# @dp.message_handler(commands=['weather'])
async def weather(message:types.Message):
    await bot.send_message(message.from_user.id, 'Здесь должна быть погода', reply_markup=(help_kb))
    await message.delete()
    print(message.from_user.first_name + ' запросил погоду')


# Приветствие новеньких
# @dp.message_handler(content_types=['new_chat_members'])
async def user_joined(message:types.Message):
    await message.answer(message.from_user.first_name + ', добро пожаловать в чат!\n\
Я буду следить за порядком в чате Три Версты \
и предоставлять полезную информацию!\n\
Чтобы увидеть список моих команд нажми кнопку /Помощь', reply_markup=(help_kb))
    print(message.from_user.first_name + ' вошел в чат')


# Прощание с покинувшими чат
# @dp.message_handler(content_types=['left_chat_member'])
async def user_left(message:types.Message):
    await message.answer(message.from_user.first_name + ', мы будем по тебе скучать!')
    try:
        await bot.send_message(message.from_user.first_name + ', мы будем по тебе скучать!')
    except:
        print(message.from_user.first_name + ' не получил прощание в ЛС')
    print(message.from_user.first_name + ' покинул чат')


# Регистрация хендлеров для последующего импорта в tri_verstyBot.py
def register_handlers_client(dp:Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(announcements, commands=['Анонсы'])
    dp.register_message_handler(help, commands=['Помощь'])
    dp.register_message_handler(vk_group, commands=['ВК'])
    dp.register_message_handler(weather, commands=['Погода'])
    dp.register_message_handler(user_joined, content_types=['new_chat_members'])
    dp.register_message_handler(user_left, content_types=['left_chat_member'])
