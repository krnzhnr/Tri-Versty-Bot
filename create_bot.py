from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot('5248251249:AAEjdP_4Ul0UxWDHPOr-kyAEWN9nkm7LPpY')
dp = Dispatcher(bot, storage=storage)
