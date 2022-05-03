import asyncio
import datetime
import sqlite3 as sq
from contextlib import suppress

from aiogram import types
from aiogram.utils.exceptions import (MessageToEditNotFound, MessageCantBeEdited, MessageCantBeDeleted,
                                      MessageToDeleteNotFound)

from create_bot import bot, dp


async def delete_message(message: types.Message, sleep_time: int = 0):
    await asyncio.sleep(sleep_time)
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await message.delete()


# Подключение к базе данных
def sql_start():
    global base, cur
    base = sq.connect('tri_versty.db')
    cur = base.cursor()
    if base:
        print('Data base connected')
    base.execute('CREATE TABLE IF NOT EXISTS database(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)')
    base.commit()


# Добавление в базу данных
async def sql_add_command(state):
    nowdatetime = datetime.datetime.now()
    now = nowdatetime.strftime('[%d/%m/%Y %H:%M:%S]')
    async with state.proxy() as data:
        try:
            cur.execute('INSERT INTO database VALUES(?, ?, ?, ?)', tuple(data.values()))
            base.commit()
            print(now, 'Успешная запись в базу ANNOUNCEMENTS-DB')
        except Exception as exc: 
            print(now, 'ОШИБКА: Запись в базу ANNOUNCEMENTS-DB не произведена')
            print(exc)


# Чтение базы данных пользователем командой /Анонсы
async def sql_read(message):
    nowdatetime = datetime.datetime.now()
    now = nowdatetime.strftime('[%d/%m/%Y %H:%M:%S]')
    try:
        for ret in cur.execute('SELECT * FROM database').fetchall():
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\n\n{ret[2]}\n\n{ret[-1]}')
        print(now, 'Успешное чтение ANNOUNCEMENTS-DB пользователем')
    except Exception as exc:
        msg = await message.answer('Общение с ботом через ЛС, напиши ему:\n@triversty_bot')
        asyncio.create_task(delete_message(msg, 15))
        await message.delete()
        print(now, 'ОШИБКА: Чтение из базы ANNOUNCEMENTS-DB не произведено')
        print(exc, f'{message.from_user.first_name}')


# Чтение базы данных админом командой /Удалить
async def sql_read2():
    nowdatetime = datetime.datetime.now()
    now = nowdatetime.strftime('[%d/%m/%Y %H:%M:%S]')
    try:
        print(now, 'Успешное чтение ANNOUNCEMENTS-DB админом для удаления')
        return cur.execute('SELECT * FROM database').fetchall()
    except Exception as exc:
        print(now, 'ОШИБКА: Чтение базы ANNOUNCEMENTS-DB админом для удаления не произведено')
        print(exc)


# Удаление из базы данных инлайн кнопкой "Удалить"
async def sql_delete_command(data):
    nowdatetime = datetime.datetime.now()
    now = nowdatetime.strftime('[%d/%m/%Y %H:%M:%S]')
    try:
        cur.execute('DELETE FROM database WHERE name == ?', (data,))
        base.commit()
        print(now, 'Успешное удаление из базы ANNOUNCEMENTS-DB')
    except Exception as exc:
        print(now, 'ОШИБКА: Удаление ' + data + ' из базы ANNOUNCEMENTS-DB не произведено')
        print(exc)
