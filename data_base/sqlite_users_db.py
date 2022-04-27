import datetime
import sqlite3 as sq

from create_bot import bot, dp

def sql_users_start():
    global userbase, usercur
    userbase = sq.connect('user_tri_versty.db')
    usercur = userbase.cursor()
    if userbase:
        print('User database connected')
    userbase.execute('CREATE TABLE IF NOT EXISTS users(id PRIMARY KEY, username, first_name)')
    userbase.commit()


async def sql_add_user(userdata):
    nowdatetime = datetime.datetime.now()
    now = nowdatetime.strftime('[%d/%m/%Y %H:%M:%S]')
    user_id = userdata['id']
    try:
        usercur.execute('INSERT INTO users VALUES (?,?,?)', tuple(userdata.values()))
        userbase.commit()
        print(now, 'Adding user with id %s to users table' % user_id)
    except sq.IntegrityError as exc:
        print(now, exc)
        print(now, 'User with id %s already exists' % user_id)
        return True
    except Exception as exc:
        print(now, 'ERROR:', exc)
    else:
        print(now, f"{userdata['first_name']}" ' добавлен в базу, ошибок не было: вы великолепны!')


async def read_users():
    return usercur.execute('SELECT first_name FROM users').fetchall()


async def read_users_mailing_list():
    return usercur.execute('SELECT id, first_name FROM users').fetchall()
        

    
    
    
    
    
    
    