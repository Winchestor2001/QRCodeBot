from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext

from database.connections import get_all_users, save_channel, get_all_channels, del_channel
from keyboards.inline_btns import admin_panel_btn, channels_list_btn
from keyboards.reply_btns import cancel_btn, remove_btn
from loader import bot
from aiogram.types import Message, CallbackQuery
from data.config import ADMINS
from states.AllStates import UserStates


async def admin_panel_handler(message: Message):
    user_id = message.from_user.id
    if user_id in ADMINS:
        all_users = await get_all_users()
        btn = await admin_panel_btn()
        await message.answer(f"Total users: {all_users}", reply_markup=btn)


async def add_channel_callback(c: CallbackQuery):
    btn = await cancel_btn()
    await c.message.delete()
    await c.message.answer("Send me: channel id + channel name + channel url", reply_markup=btn)
    await UserStates.add_channel.set()


async def add_channel_state(message: Message, state: FSMContext):
    _ = message.text.replace(" + ", "+")
    if _ in ["❌ Cancel", "/start"]:
        await message.answer("❌ Canceled", reply_markup=remove_btn)
        await admin_panel_handler(message)
        return await state.finish()

    text = _.split("+")
    if len(text) == 3:
        await save_channel(text[0], text[1], text[2])
        await message.answer("✅ Channel added successfully")
        await admin_panel_handler(message)
        await state.finish()
    else:
        await message.answer("❗️ Channel data incorrect")


async def show_channels_callback(c: CallbackQuery):
    channels = await get_all_channels()
    if channels:
        btn = await channels_list_btn(channels)
        context = ""
        for i, channel in enumerate(channels, 1):
            context += f"{i}) <a href='{channel['channel_url']}'>{channel['channel_name']}</a>"

        await c.message.edit_text(context, reply_markup=btn, disable_web_page_preview=True)
    else:
        await c.answer("Channels is empty", show_alert=True)


async def del_channel_callback(c: CallbackQuery):
    channel_id = c.data.split(':')[-1]
    await del_channel(channel_id)
    await c.message.edit_text("✅ Channel was deleted successfully")
    await admin_panel_handler(c.message)


def register_admin_handlers_py(dp: Dispatcher):
    dp.register_message_handler(admin_panel_handler, commands=['admin'])

    dp.register_message_handler(add_channel_state, state=UserStates.add_channel)

    dp.register_callback_query_handler(add_channel_callback, text='add_channel')
    dp.register_callback_query_handler(show_channels_callback, text='channels_list')
    dp.register_callback_query_handler(del_channel_callback, text_contains='del_channel:')
