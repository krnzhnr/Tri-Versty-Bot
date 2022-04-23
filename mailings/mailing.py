from create_bot import dp
from aiogram import types, Dispatcher
from data_base import sqlite_users_db


@dp.message_handler(commands=['mailing'])
async def mailing(message:types.Message):
    await  sqlite_users_db.read_users_mailing_list()


def register_handlers_mailing(dp:Dispatcher):
    dp.register_message_handler(mailing, commands=['mailing'])
    