import sqlite3 as sq

from create_bot import bot, dp


def sql_start():
    global base, cur
    base = sq.connect('tri_versty.db')
    cur = base.cursor()
    if base:
        print('Data base connected')
    base.execute('CREATE TABLE IF NOT EXISTS database(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)')
    base.execute('CREATE TABLE IF NOT EXISTS regdatabase(link TEXT)')
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO database VALUES(?, ?, ?, ?)', tuple(data.values()))
        base.commit()


async def sql_read(message):
    for ret in cur.execute('SELECT * FROM database').fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\n{ret[2]}\nВзять с сообой: {ret[-1]} руб.')


async def sql_read2():
    return cur.execute('SELECT * FROM database').fetchall()


async def sql_delete_command(data):
    cur.execute('DELETE FROM database WHERE name == ?', (data,))
    base.commit()


########################################################################


async def sql_reg_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO regdatabase VALUES(?)', tuple(data.values()))
        base.commit()


async def sql_reg_read(message):
    for reg in cur.execute('SELECT * FROM regdatabase').fetchall():
        await bot.send_message(message.from_user.id, f'Держи ссылку на форму для регистрации:\n{reg[0]}')


async def sql_reg_read2():
    return cur.execute('SELECT * FROM regdatabase').fetchall()


async def sql_delete_reg_command(data):
    cur.execute('DELETE FROM regdatabase WHERE link == ?', (data,))
    base.commit()
