from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)
from create_bot import bot, dp
from data_base import sqlite_db

upload_button = KeyboardButton('/Загрузить')
reg_button = KeyboardButton('/reg_load')
delete_reg_button = KeyboardButton('/deletereg')
cancel_button = KeyboardButton('/Отмена')
delete_button = KeyboardButton('/Удалить')
admin_kb = ReplyKeyboardMarkup(resize_keyboard=False)\
    .add(upload_button, cancel_button, delete_button)\
    .add(reg_button, delete_reg_button)

ID = None

class FSMReg(StatesGroup):
    reg_link = State()

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


# @dp.message_handler(commands=['reg_load'], state=None)
async def reg(message:types.Message):
    if message.from_user.id == ID:
        await FSMReg.reg_link.set()
        await message.reply('Я получил команду, кидай ссылку')

# @dp.message_handler(state=FSMReg.reg_link)
async def reg_link_load(message:types.Message, state:FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as regdata:
            regdata['link'] = message.text
        await sqlite_db.sql_reg_command(state)
        await state.finish()


# @dp.message_handler(commands='Загрузить', state=None)
async def cm_start(message:types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply('Загрузи фото')


async def cancel_handler(message:types.Message, state:FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('ОК')


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


# @dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query:types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удалена.', show_alert=True)


# Удаление ссылки на регистрацию
# @dp.callback_query_handler(lambda z: z.data and z.data.startswith('del '))
async def del_reg_callback_run(reg_callback_query:types.CallbackQuery):
    await sqlite_db.sql_delete_reg_command(reg_callback_query.data.replace('del ', ''))
    await reg_callback_query.answer(text=f'{reg_callback_query.data.replace("del ", "")} удалена.', show_alert=True)
    await reg_callback_query.answer()


# @dp.message_handler(commands=['deletereg'])
async def delete_reg(message:types.Message):
    if message.from_user.id == ID:
        read = await sqlite_db.sql_reg_read2()
        for regret in read:
            await bot.send_message(message.from_user.id, f'{regret[0]}')
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup().\
                add(InlineKeyboardButton(f'Удалить {regret[0]}', callback_data=f'del {regret[0]}')))


# @dp.message_handler(commands=['Удалить'])
async def delete_item(message:types.Message):
    if message.from_user.id == ID:
        read = await sqlite_db.sql_read2()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nВзять с сообой: {ret[-1]} руб')
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup().\
                add(InlineKeyboardButton(f'Удалить {ret[1]}', callback_data=f'del {ret[1]}')))


def register_handlers_admin(dp:Dispatcher):
    dp.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin = True)
    dp.register_message_handler(reg, commands=['reg_load'], state=None)
    dp.register_message_handler(reg_link_load, state=FSMReg.reg_link)
    dp.register_message_handler(cm_start, commands=['Загрузить'], state=None)
    dp.register_message_handler(cancel_handler, state="*", commands=['Отмена'])
    dp.register_message_handler(cancel_handler, Text(equals = 'Отмена', ignore_case = True), state = "*")
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_callback_query_handler(del_callback_run, lambda x: x.data and x.data.startswith('del '))
    dp.register_callback_query_handler(delete_reg, lambda z: z.data and z.data.startswith('del '))
    dp.register_message_handler(delete_reg, commands=['deletereg'])
    dp.register_message_handler(delete_item, commands='Удалить')
