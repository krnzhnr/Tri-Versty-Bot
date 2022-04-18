from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)
from create_bot import bot
from data_base import sqlite_db

upload_button = KeyboardButton('/Загрузить')
cancel_button = KeyboardButton('/Отмена')
delete_button = KeyboardButton('/Удалить')
admin_kb = ReplyKeyboardMarkup(resize_keyboard=False).\
    add(upload_button, delete_button).\
    add(cancel_button)

ID = None

class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


# @dp.message_handler(commands=['moderator'], is_chat_admin = True)
async def make_changes_command(message:types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Что хозяин надо???', reply_markup=admin_kb)
    await message.delete()
    print(message.from_user.first_name + ' запустил админку')


#################################################################### Добавление в ANNOUNCEMENTS-DB #################################################################################


# @dp.message_handler(commands='Загрузить', state=None)
async def cm_start(message:types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply('Загрузи фото')
        print(message.from_user.first_name + ' начал добавление в ANNOUNCEMENTS-DB')


async def cancel_handler(message:types.Message, state:FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('ОК')
        print(message.from_user.first_name + ' отменил добавление в ANNOUNCEMENTS-DB')


# @dp.message_handler(content_types=['photo'],state=FSMAdmin.photo)
async def load_photo(message:types.Message, state:FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply('Теперь введи название')


# @dp.message_handler(state=FSMAdmin.name)
async def load_name(message:types.Message, state:FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply('Введи описание')


# @dp.message_handler(state=FSMAdmin.description)
async def load_description(message:types.Message, state:FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await message.reply('Теперь укажи сколько взять с собой')


# @dp.message_handler(state=FSMAdmin.price)
async def load_price(message:types.Message, state:FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = message.text
        await sqlite_db.sql_add_command(state)
        await state.finish()
        print(message.from_user.first_name + ' добавил объект в анонсы')


##################################################################### Запрос на удаление из базы данных ############################################################################


# @dp.message_handler(commands=['Удалить'])
async def delete_item(message:types.Message):
    if message.from_user.id == ID:
        read = await sqlite_db.sql_read2()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nВзять с сообой: {ret[-1]} руб')
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup().\
                add(InlineKeyboardButton(f'Удалить {ret[1]}', callback_data=f'del {ret[1]}')))
    print(message.from_user.first_name + ' запросил ANNOUNCEMENTS-DB для удаления')


######################################################################## Удаление из базы данных ###################################################################################


# @dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query:types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удалена.', show_alert=True)
    

####################################################################### Регистрация хэндлеров ######################################################################################


def register_handlers_admin(dp:Dispatcher):
    dp.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin = True)
    dp.register_message_handler(cm_start, commands=['Загрузить'], state=None)
    dp.register_message_handler(cancel_handler, state="*", commands=['Отмена'])
    dp.register_message_handler(cancel_handler, Text(equals = 'Отмена', ignore_case = True), state = "*")
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(delete_item, commands='Удалить')
    dp.register_callback_query_handler(del_callback_run, lambda x: x.data and x.data.startswith('del '))
