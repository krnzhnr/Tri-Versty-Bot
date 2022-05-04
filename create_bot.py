from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot('5328605145:AAEW-pJCnYLnFW_SbQWyB0NYbiOoEq5cE9k')
dp = Dispatcher(bot, storage=storage)
