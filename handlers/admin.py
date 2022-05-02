import datetime

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)
from create_bot import bot, dp
from data_base import sqlite_announcements_db, sqlite_users_db


upload_button = KeyboardButton('/Загрузить')
cancel_button = KeyboardButton('/Отмена')
delete_button = KeyboardButton('/Удалить')
mailing_button = KeyboardButton('/Рассылка')
users_button = KeyboardButton('/users')
admin_kb = ReplyKeyboardMarkup(resize_keyboard=False).\
    add(upload_button, delete_button).\
    add(users_button, mailing_button).\
    add(cancel_button)

ID = None

class FSMMailing(StatesGroup):
    mail = State()

class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    description2 = State()


# @dp.message_handler(commands=['moderator'], is_chat_admin = True)
async def get_admin(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Что хозяин надо???', reply_markup=admin_kb)
    await message.delete()
    nowdatetime = datetime.datetime.now()
    now = nowdatetime.strftime('[%d/%m/%Y %H:%M:%S]')
    print(now, message.from_user.first_name + ' запустил админку')


async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        # print(current_state)
        if current_state is None:
            return
        await state.finish()
        await message.reply('ОК')
        nowdatetime = datetime.datetime.now()
        now = nowdatetime.strftime('[%d/%m/%Y %H:%M:%S]')
        print(now, message.from_user.first_name + ' отменил действие')


############################################################################# РАССЫЛКА #############################################################################################


# @dp.message_handler(commands=['Рассылка'], state=None)
async def setmail(message: types.Message):
    nowdatetime = datetime.datetime.now()
    now = nowdatetime.strftime('[%d/%m/%Y %H:%M:%S]')
    if message.from_user.id == ID:
        await FSMMailing.mail.set()
        await message.reply('Напиши мне то, что нужно разослать')
        print(now, message.from_user.first_name + ' начал формирование рассылки')


# @dp.message_handler(state=FSMMailing.mail)
async def mail(message: types.Message, state=FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as mail:
            mail['mail_text'] = message.text
            users = await sqlite_users_db.read_users_mailing_list()
            successful = 0
            failed = 0
            for user in users:
                usr = {'id': user[0], 'first_name': user[1]}
                try:
                    await bot.send_message(f'{usr["id"]}', 
                                           f'{mail["mail_text"]}')
                    await message.answer(f'{usr["first_name"]}' + ' получил сообщение')
                    successful += 1
                except Exception as exc:
                    await message.answer(f'{exc} ' + 
                                         f'{usr["first_name"]}')
                    failed += 1
            await message.answer('Успешно отправлено: ' + str(successful) + 
                                 '\nНе отправлено: ' + str(failed))
            nowdatetime = datetime.datetime.now()
            now = nowdatetime.strftime('[%d/%m/%Y %H:%M:%S]')
            print(now, f'{message.from_user.first_name} успешно разослал {successful} сообщений с текстом: {mail["mail_text"]}')
            await state.finish()


######################################################################## Список пользователей ######################################################################################
    

# @dp.message_handler(commands=['users'])
async def read_users(message: types.Message):
    user_list = await sqlite_users_db.read_users()
    count = 0
    for user in user_list:
        await message.answer(f'{user[0]}')
        count += 1
    await message.answer(f'{count} пользователя')


#################################################################### Добавление в ANNOUNCEMENTS-DB #################################################################################


# @dp.message_handler(commands='Загрузить', state=None)
async def cm_start(message: types.Message):
    nowdatetime = datetime.datetime.now()
    now = nowdatetime.strftime('[%d/%m/%Y %H:%M:%S]')
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply('Загрузи фото')
        print(now, message.from_user.first_name + ' начал добавление в ANNOUNCEMENTS-DB')


# @dp.message_handler(content_types=['photo'],state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply('Теперь введи название, оно должно быть не длиннее 30 символов')


# @dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            if len(message.text) < 30:
                data['name'] = message.text.upper()
        await FSMAdmin.next()
        await message.reply('Введи описание')


# @dp.message_handler(state=FSMAdmin.description)
async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await message.reply('Теперь введи что-нибудь еще')


# @dp.message_handler(state=FSMAdmin.description2)
async def load_description2(message: types.Message, state: FSMContext):
    nowdatetime = datetime.datetime.now()
    now = nowdatetime.strftime('[%d/%m/%Y %H:%M:%S]')
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = message.text
        await sqlite_announcements_db.sql_add_command(state)
        await state.finish()
        print(now, message.from_user.first_name + ' добавил объект в анонсы')


##################################################################### Запрос на удаление из базы данных ############################################################################


# @dp.message_handler(commands=['Удалить'])
async def delete_item(message: types.Message):
    nowdatetime = datetime.datetime.now()
    now = nowdatetime.strftime('[%d/%m/%Y %H:%M:%S]')
    if message.from_user.id == ID:
        print(now, message.from_user.first_name + ' запросил ANNOUNCEMENTS-DB для удаления')
        read = await sqlite_announcements_db.sql_read2()
        for ret in read:
            await bot.send_photo(message.from_user.id, 
                                 ret[0], 
                                 f'{ret[1]}\
                                \nОписание: {ret[2]}\
                                \nОписание: {ret[-1]}')
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup().\
                add(InlineKeyboardButton(f'Удалить {ret[1]}', callback_data=f'del {ret[1]}')))


######################################################################## Удаление из базы данных ###################################################################################


# @dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    await sqlite_announcements_db.sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удалена.', show_alert=True)
    

####################################################################### Регистрация хэндлеров ######################################################################################


def register_handlers_admin(dp:Dispatcher):
    dp.register_message_handler(get_admin, commands=['admin'], is_chat_admin = True)
    dp.register_message_handler(cancel_handler, state="*", commands=['Отмена'])
    dp.register_message_handler(cancel_handler, Text(equals = 'Отмена', ignore_case = True), state = "*")
    dp.register_message_handler(setmail, commands=['Рассылка'], state=None)
    dp.register_message_handler(mail, state=FSMMailing.mail)
    dp.register_message_handler(read_users, commands=['users'])
    dp.register_message_handler(cm_start, commands=['Загрузить'], state=None)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_description2, state=FSMAdmin.description2)
    dp.register_message_handler(delete_item, commands=['Удалить'])
    dp.register_callback_query_handler(del_callback_run, lambda x: x.data and x.data.startswith('del '))
