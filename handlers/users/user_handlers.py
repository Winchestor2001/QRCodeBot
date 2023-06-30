from aiogram.dispatcher import FSMContext

from database.connections import add_user
from keyboards.inline_btns import qrcode_settings_btn
from loader import bot, dp
from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery, InputFile, InputMediaPhoto
from keyboards.reply_btns import *
from states.AllStates import UserStates
from utils.usefull_funcs import make_simple_qrcode, check_qrcode_option, qr_option_btn_names, is_equal_option, \
    spliting_by_option


async def start_bot_handler(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username

    btn = await start_menu_btn()
    await add_user(user_id, username)
    await message.answer("Hi", reply_markup=btn)


async def info_handler(message: Message):
    await message.answer("Info")


async def support_handler(message: Message):
    await message.answer("Info")


async def qrcode_options_handler(message: Message):
    btn = await qrcode_options_btn()
    await message.answer("Select QR option:", reply_markup=btn)
    await UserStates.select_qr_option.set()


async def qrcode_options_state(message: Message, state: FSMContext):
    text = message.text
    if text == '🔙 Back':
        await state.reset_state(with_data=False)
        return await start_bot_handler(message)
    if text in qr_option_btn_names:
        await state.update_data(qrcode_options=text, scale=8, dark_color="#000", light_color="#fff")

        btn = await cancel_btn()
        context = await is_equal_option(text)
        await message.answer(context, reply_markup=btn)
        await UserStates.get_text.set()


async def get_qrcode_text_state(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text
    if text in ['❌ Cancel', '/start']:
        await state.finish()
        return await start_bot_handler(message)

    data = await state.get_data()
    split_opt = await spliting_by_option(data['qrcode_options'], text)
    if split_opt:
        filename = await check_qrcode_option(user_id, data['qrcode_options'], split_opt)
        btn = await start_menu_btn()
        await message.answer("👇", reply_markup=btn)

        btn = await qrcode_settings_btn()
        await message.answer_photo(InputFile(filename), reply_markup=btn)
        await state.reset_state(with_data=False)
        await state.update_data(text=split_opt)
    else:
        await message.answer("Incorrect data")


async def qrcode_setting_scale_callback(c: CallbackQuery, state: FSMContext):
    user_id = c.from_user.id
    data = await state.get_data()
    scale_options = data['scale'] + 2 if c.data.split(":")[-1] == 'plus' else data['scale'] - 2
    await state.update_data(scale=scale_options)
    filename = await check_qrcode_option(user_id, data['qrcode_options'], data['text'], scale=scale_options,
                                         dark_color=data['dark_color'],
                                         light_color=data['light_color'])
    btn = await qrcode_settings_btn()
    await c.message.edit_media(InputMediaPhoto(InputFile(filename)), reply_markup=btn)


async def qrcode_setting_color_callback(c: CallbackQuery, state: FSMContext):
    await c.answer()
    user_id = c.from_user.id
    data = await state.get_data()
    color = c.data.split(":")[-1]
    if data['dark_color'] != color:
        filename = await check_qrcode_option(user_id, data['qrcode_options'], data['text'], scale=data['scale'],
                                             dark_color=color,
                                             light_color=data['light_color'])
        await state.update_data(dark_color=color)
        btn = await qrcode_settings_btn()
        await c.message.edit_media(InputMediaPhoto(InputFile(filename)), reply_markup=btn)


async def qrcode_finish_callback(c: CallbackQuery, state: FSMContext):
    user_id = c.from_user.id
    bot_username = (await bot.get_me()).username
    filename = f"qr_{user_id}.png"
    await c.message.edit_caption(f"By @{bot_username}")
    await c.message.answer_document(InputFile(filename, f"@{bot_username}.png"))
    await state.finish()


def register_users_py(dp: Dispatcher):
    dp.register_message_handler(start_bot_handler, commands=['start'])

    dp.register_message_handler(start_bot_handler, text="🔙 Back")
    dp.register_message_handler(info_handler, text="ℹ️ Info")
    dp.register_message_handler(support_handler, text="👤 Support")
    dp.register_message_handler(qrcode_options_handler, text="✏️ QR Code generation")

    dp.register_message_handler(qrcode_options_state, state=UserStates.select_qr_option, content_types=['text'])
    dp.register_message_handler(get_qrcode_text_state, state=UserStates.get_text, content_types=['text'])

    dp.register_callback_query_handler(qrcode_finish_callback, text="qr_finish")
    dp.register_callback_query_handler(qrcode_setting_scale_callback, text_contains="scale")
    dp.register_callback_query_handler(qrcode_setting_color_callback, text_contains="color")