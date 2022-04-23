import sqlite3 as sq
from create_bot import dp, bot

def sql_users_start():
    global userbase, usercur
    userbase = sq.connect('user_tri_versty.db')
    usercur = userbase.cursor()
    if userbase:
        print('User database connected')
    userbase.execute('CREATE TABLE IF NOT EXISTS users(id, username, first_name)')
    userbase.commit()


async def sql_add_user(userdata):
    id_check(userdata)
    user_id = userdata['id']
    if id_check(userdata) is True:
        print('Adding user with id %s to users table' % user_id)
        usercur.execute('INSERT INTO users VALUES (?,?,?)', tuple(userdata.values()))
        userbase.commit()
    else:
        print('User with id %s already exists' % user_id)


def id_check(userdata):
    user_id = userdata['id']
    est = usercur.execute('SELECT id FROM users WHERE id = ?', (user_id,))
    if est.fetchone() is None:
        return True
    else:
        return False


async def read_users():
    return usercur.execute('SELECT first_name FROM users').fetchall()


async def read_users_mailing_list():
    count = 0
    for user in usercur.execute('SELECT id, first_name FROM users').fetchall():
        usr = {'id': user[0], 'first_name': user[1]}
        try:
            await bot.send_message(f'{usr["id"]}', f'Здарова {usr["first_name"]}, я тут немного рассылками балуюсь.\n\
Ты не обижайся и жди сообщений в будущем.\nЕсли не хочешь, чтобы я тебе писал, скажи об этом в чат: https://t.me/+8xKEbnzpZFRjY2Qy')
            print(f'{usr["first_name"]}' + ' получил сообщение')
            count += 1
        except Exception as exc:
            print(exc, f'{usr["first_name"]}')
    print(count)
        

    
    
    
    
    
    
    