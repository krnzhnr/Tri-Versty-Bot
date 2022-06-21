import mysql.connector
from create_bot import bot
# from handlers.client import help_kb

def mysql_start():
    try:
        global base, cursor
        base = mysql.connector.connect(
            host='localhost',
            user='admin',
            password='sqladmin',
            database='triversty'
        )
        cursor = base.cursor()    
        cursor.execute('CREATE DATABASE IF NOT EXISTS triversty')
        cursor.execute("CREATE TABLE IF NOT EXISTS announcements(\
            img VARCHAR(255),\
            name VARCHAR(255),\
            description VARCHAR(1000),\
            description2 VARCHAR(1000))"
        )
        cursor.execute("CREATE TABLE IF NOT EXISTS users(\
            id INT PRIMARY KEY,\
            username VARCHAR(255),\
            first_name VARCHAR(255))"
        )
        base.commit()
        print('triversty database connected')
        show_tables()
    except Exception as exc:
        print(exc)
        print('ERROR: Unable to connect to MySQL')

    
def query_handler(query):
    return cursor.execute(query)


def show_tables():
    query_handler("SHOW TABLES")
    for table in cursor:
        print(table)


async def mysql_add_user(userdata):
    user_id = userdata['id']
    user_firstname = userdata['first_name']
    try:
        query = '''INSERT INTO users (
            id, 
            username, 
            first_name
        ) VALUES ('{}', '{}', '{}')'''.format(*userdata.values())
        query_handler(query)
        base.commit()
        print('Adding user with id {} to users table'.format(user_id))
    except mysql.connector.Error as exc:
        print('ERROR: Unable to add user {} to users table'.format(user_firstname))
        print(exc)
        return True


async def mysql_read_users():
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    return users


async def mysql_read_mailing():
    query = 'SELECT id, first_name FROM users'
    query_handler(query)
    return cursor.fetchall()


##############################################################################


async def mysql_add_announce(state):
    async with state.proxy() as announce:
        try:
            query = '''INSERT INTO announcements (
                img, 
                name, 
                description, 
                description2
            ) VALUES ('{}', '{}', '{}', '{}')'''.format(*announce.values())
            query_handler(query)
            base.commit()
        except Exception as exc:
            print('ERROR: {}'.format(exc))


async def mysql_read_announcements(message):
    query = 'SELECT * FROM announcements'
    query_handler(query)
    items = cursor.fetchall()
    print(items)
    try:
        for item in items:
            await bot.send_photo(
                message.from_user.id, 
                item[0], 
                f'{item[1]}\n\n{item[2]}\n\n{item[-1]}')
    except Exception as exc:
        await message.answer('Шо то не работает, глянь в консольку')
        print('ERROR: {}'.format(exc))
