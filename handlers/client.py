import asyncio
import datetime
from contextlib import suppress

from aiogram import Dispatcher, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.exceptions import (MessageCantBeDeleted,
                                      MessageToDeleteNotFound)
from create_bot import bot, dp
from data_base import sqlite_announcements_db, sqlite_users_db

admin_button = KeyboardButton('/moderator')
start_button = KeyboardButton('/start')

registration_button = KeyboardButton('/Регистрация')
category_button = KeyboardButton('/Категории')
help_button = KeyboardButton('/Помощь')
social_button = KeyboardButton('/Соцсети')
weather_button = KeyboardButton('/Погода')
announcements_button = KeyboardButton('/Анонсы')
help_kb = ReplyKeyboardMarkup(resize_keyboard=True).\
    row(registration_button).\
    row(announcements_button, weather_button).\
    row(social_button, category_button).\
    row(help_button)
chat_kb = ReplyKeyboardMarkup(resize_keyboard=True).\
    row(registration_button).\
    row(announcements_button, social_button).\
    row(help_button, category_button)


# Удаление своих сообщений через промежуток времени
async def delete_message(message: types.Message, sleep_time: int = 0):
    await asyncio.sleep(sleep_time)
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await message.delete()


# Команда /chat_start
async def chat_start(message: types.Message):
    await message.answer("""
Привет всем! Я буду следить за порядком в чате Три Версты \
и предоставлять полезную информацию!
Чтобы начать работу, напишите мне в личку.
После запуска диалога со мной вы также сможете использовать кнопки в чате.""", reply_markup=chat_kb)
    await message.delete()
    

# Команда /start
async def start(message: types.Message):
    nowdatetime = datetime.datetime.now()
    now = nowdatetime.strftime('[%d/%m/%Y %H:%M:%S]')
    try:
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
            await bot.send_message(message.from_user.id, 
                                   f"{message.from_user.first_name}"
                                   ', привет! Я буду следить за порядком в чате Три Версты \
и предоставлять полезную информацию!\nДля управления ботом используй кнопки.', 
                                    reply_markup=help_kb)
    except Exception as exc:
        msg = await message.answer('Чтобы использовать бота напиши ему в ЛС:\n@triversty_bot', 
                                   reply_markup=help_kb)
        asyncio.create_task(delete_message(msg, 15))
        await message.delete()
        print(now, exc, f'{message.from_user.first_name}')
    

# Команда /Регистрация
async def registration_link(message:types.Message):
    nowdatetime = datetime.datetime.now()
    now = nowdatetime.strftime('[%d/%m/%Y %H:%M:%S]')
    try:
        await bot.send_message(message.from_user.id, """
Для предварительной регистрации на гонку заполните форму:

https://forms.gle/5TaqUKdgFPwoSWSo6
""", reply_markup = help_kb)
        await message.delete()
        print(now, message.from_user.first_name + ' запросил регистрацию')
    except Exception as exc:
        msg = await message.answer('Общение с ботом через ЛС, напиши ему:\n@triversty_bot')
        asyncio.create_task(delete_message(msg, 15))
        await message.delete()
        print(now, message.from_user.first_name + ' не смог запросить регистрацию')
        print(now, exc, f'{message.from_user.first_name}')
 

# Команда /Анонсы
async def announcements(message: types.Message):
    nowdatetime = datetime.datetime.now()
    now = nowdatetime.strftime('[%d/%m/%Y %H:%M:%S]')
    try:
        await sqlite_announcements_db.sql_read(message)
        print(now, message.from_user.first_name + ' запросил анонсы')
        await message.delete()
    except Exception as exc:
        print(now, exc, f'{message.from_user.first_name}')
    

# Команда /Помощь
async def help(message: types.Message):
    nowdatetime = datetime.datetime.now()
    now = nowdatetime.strftime('[%d/%m/%Y %H:%M:%S]')
    try:
        await bot.send_message(message.from_user.id, """
    Вот список моих команд:

/Регистрация - получите ссылку для предварительной регистрации на предстоящую гонку

/Анонсы - получите в ЛС все актуальные на данный момент анонсы

/ВК - Наша группа ВК со всеми фотографиями

/Погода - Текущая погода в городе, который ты напишешь

/Помощь - Помощь по командам

⚠️ Организаторы могут использовать бота для осуществления информационных рассылок!
""", reply_markup=help_kb)
        await message.delete()
        print(now, message.from_user.first_name + ' запросил помощь')
    except Exception as exc:
        msg = await message.answer('Общение с ботом через ЛС, напиши ему:\n@triversty_bot')
        asyncio.create_task(delete_message(msg, 15))
        await message.delete()
        print(now, message.from_user.first_name + ' не смог запросить помощь')
        print(now, exc, f'{message.from_user.first_name}')


# Команда /Соцсети
async def social_group(message: types.Message):
    nowdatetime = datetime.datetime.now()
    now = nowdatetime.strftime('[%d/%m/%Y %H:%M:%S]')
    try:
        await bot.send_message(message.from_user.id, """
Вот тут вы нас найдёте

Наша группа ВК с фоточками:
https://vk.com/kubok_tri_versty

Наш инстаграмм с фоточками и видосами:
https://www.instagram.com/triversty_cup/
""", reply_markup=help_kb)
        await message.delete()
        print(now, message.from_user.first_name + ' запросил соцсети')
    except Exception as exc:
        msg = await message.answer('Общение с ботом через ЛС, напиши ему:\n@triversty_bot')
        asyncio.create_task(delete_message(msg, 15))
        await message.delete()
        print(now, message.from_user.first_name + ' не смог запросить соцсети')
        print(now, exc, f'{message.from_user.first_name}')


# Команда /Категории
async def category(message: types.Message):
    nowdatetime = datetime.datetime.now()
    now = nowdatetime.strftime('[%d/%m/%Y %H:%M:%S]')
    try:
        await bot.send_message(message.from_user.id, """
Категории

Мужчины:

Дети 10-12 лет (2010-2012 год рождения)
Подростки 13-14 лет (2008-2009 год рождения)
Юниоры 15-17 лет (2005-2007 год рождения)
Андеры 18-23 лет (1999-2004 год рождения)
Элита 24-34 лет (1988-1998 год рождения)
Элита+ 35-44 лет (1978-1987 год рождения)
Мастер 45-54 лет (1968-1977 год рождения)
Мастер+ 55+ лет (1967 год рождения и старше)

Женщины:

Девочки 10-14 лет (2008-2012 год рождения)
Юниорки 15-18 лет (2004-2007 год рождения)
Спорт 19-29 лет (1993-2003 год рождения)
Фитнес 30-39 лет (1983-1992 год рождения)
Суперфит 40+ лет (1982 год рождения и старше)""", reply_markup = help_kb)
        await message.delete()
        print(now, message.from_user.first_name + ' запросил категории')
    except Exception as exc:
        msg = await message.answer('Общение с ботом через ЛС, напиши ему:\n@triversty_bot')
        asyncio.create_task(delete_message(msg, 15))
        await message.delete()
        print(now, exc, f'{message.from_user.first_name}')
        print(now, message.from_user.first_name + ' не смог запросить категории')


# @dp.message_handler(content_types=['new_chat_members'])
async def user_joined(message: types.Message):
    nowdatetime = datetime.datetime.now()
    now = nowdatetime.strftime('[%d/%m/%Y %H:%M:%S]')
    await message.answer("""
Добро пожаловать в чат!
Я буду следить за порядком в чате Три Версты\
и предоставлять полезную информацию!
Чтобы начать работу, напиши мне в личку.
После запуска диалога со мной ты сможешь использовать кнопки в чате.""", reply_markup=chat_kb)
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
    dp.register_message_handler(chat_start, commands=['chat_start'])
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(registration_link, commands=['Регистрация'])
    dp.register_message_handler(announcements, commands=['Анонсы'])
    dp.register_message_handler(help, commands=['Помощь'])
    dp.register_message_handler(social_group, commands=['Соцсети'])
    dp.register_message_handler(category, commands=['Категории'])
    dp.register_message_handler(user_joined, content_types=['new_chat_members'])
    dp.register_message_handler(user_left, content_types=['left_chat_member'])

