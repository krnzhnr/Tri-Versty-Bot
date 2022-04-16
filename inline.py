from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

bot = Bot('5248251249:AAEjdP_4Ul0UxWDHPOr-kyAEWN9nkm7LPpY')
dp = Dispatcher(bot)

answ = dict()


urlkb = InlineKeyboardMarkup(row_width=2)
urlbutton = InlineKeyboardButton(text='Ссылка', url='https://vk.com')
urlbutton2 = InlineKeyboardButton(text='Ссылка2', url='https://youtube.com')
x = [InlineKeyboardButton(text='Ссылка3', url='https://google.com'),\
    InlineKeyboardButton(text='Ссылка4', url='https://google.com'),\
    InlineKeyboardButton(text='Ссылка5', url='https://google.com')]

urlkb.add(urlbutton, urlbutton2).row(*x).insert(InlineKeyboardButton(text='Ссылка6', url='https://google.com'))


@dp.message_handler(commands=['links'])
async def url_command(message:types.Message):
    await message.answer('Ссылочки:', reply_markup=urlkb)

inkb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='liek', callback_data='liek_1'),\
    InlineKeyboardButton(text='ne liek', callback_data='liek_-1'))

@dp.message_handler(commands=['test'])
async def test_commands(message:types.Message):
    await message.answer("лиек чи не лиек", reply_markup=inkb)

@dp.callback_query_handler(Text(startswith='liek_'))
async def www_call(callback:types.CallbackQuery):
    res = int(callback.data.split('_')[1])
    if f'{callback.from_user.id}' not in answ:
        answ[f'{callback.from_user.id}'] = res
        await callback.answer('вы чо то выбрали')
    else:
        await callback.answer('аааххх ухххх спасибо но ты уже чо то выбрал', show_alert=True)

executor.start_polling(dp, skip_updates=True)