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
    return usercur.execute('SELECT id, first_name FROM users').fetchall()
        

    
    
    
    
    
    
    