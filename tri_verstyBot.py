import logging

from aiogram.utils import executor

from create_bot import dp
from data_base import sqlite_announcements_db, sqlite_users_db#, mysql_db
from data_base import mysql_db
from handlers import admin, client, other, weather

logging.basicConfig(level=logging.INFO)


async def on_startup(__):
    print('Бот онлайн')
    sqlite_announcements_db.sql_start()
    sqlite_users_db.sql_users_start()
    mysql_db.mysql_start()

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
weather.register_handlers_weather(dp)
other.register_handlers_other(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
