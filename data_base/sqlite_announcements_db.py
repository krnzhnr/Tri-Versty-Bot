import sqlite3 as sq

from create_bot import bot, dp


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
    async with state.proxy() as data:
        try:
            cur.execute('INSERT INTO database VALUES(?, ?, ?, ?)', tuple(data.values()))
            base.commit()
            print('Успешная запись в базу ANNOUNCEMENTS-DB')
        except Exception as exc: 
            print('ОШИБКА: Запись в базу ANNOUNCEMENTS-DB не произведена')
            print(exc)


# Чтение базы данных пользователем командой /Анонсы
async def sql_read(message):
    try:
        for ret in cur.execute('SELECT * FROM database').fetchall():
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\n{ret[2]}\nВзять с сообой: {ret[-1]} руб.')
        print('Успешное чтение ANNOUNCEMENTS-DB пользователем')
    except Exception as exc:
        await message.answer('Общение с ботом через ЛС, напиши ему:\n@penis_mudilaBot')
        print('ОШИБКА: Чтение из базы ANNOUNCEMENTS-DB не произведено')
        print(exc)


# Чтение базы данных админом командой /Удалить
async def sql_read2():
    try:
        print('Успешное чтение ANNOUNCEMENTS-DB админом для удаления')
        return cur.execute('SELECT * FROM database').fetchall()
    except Exception as exc:
        print('ОШИБКА: Чтение базы ANNOUNCEMENTS-DB админом для удаления не произведено')
        print(exc)


# Удаление из базы данных инлайн кнопкой "Удалить"
async def sql_delete_command(data):
    try:
        cur.execute('DELETE FROM database WHERE name == ?', (data,))
        base.commit()
        print('Успешное удаление из базы ANNOUNCEMENTS-DB')
    except Exception as exc:
        print('ОШИБКА: Удаление ' + data + ' из базы ANNOUNCEMENTS-DB не произведено')
        print(exc)
