from aiogram import executor

from handlers.users.user_handlers import register_users_py
from loader import dp
import handlers
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)

    register_users_py(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
