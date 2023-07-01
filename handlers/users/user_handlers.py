import os

from aiogram.dispatcher import FSMContext

from database.connections import add_user, get_all_channels
from keyboards.inline_btns import qrcode_settings_btn, support_btn, invite_channel_btn
from loader import bot, dp
from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery, InputFile, InputMediaPhoto
from keyboards.reply_btns import *
from states.AllStates import UserStates
from utils.check_invite_to_channels import check_invite
from utils.usefull_funcs import *


async def start_bot_handler(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username

    await add_user(user_id, username)
    channels = await get_all_channels()
    is_invited = await check_invite(user_id, channels)
    if is_invited:
        btn = await start_menu_btn()
        await message.answer("Hi", reply_markup=btn)
    else:
        btn = await invite_channel_btn(channels)
        await message.answer("Please subscribe:", reply_markup=btn)


async def info_handler(message: Message):
    await message.answer(
        "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
        "📑 Introducing my QR code bot! This powerful bot can create custom QR codes with various features. It allows you to generate QR codes with different colors, adding a vibrant touch to your codes. Not only that, but you can also incorporate images into your QR codes, making them visually appealing and unique. And if you want to add some dynamic elements, you can even create QR codes with animated GIFs. With this bot, you have the flexibility to customize your QR codes like never before. Start using it to create eye-catching codes for promotions, events, or personal use. Explore the possibilities and let your QR codes stand out from the crowd!\n"
        "➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖"
    )


async def support_handler(message: Message):
    btn = await support_btn()
    await message.answer("Support info", reply_markup=btn)


async def qrcode_options_handler(message: Message):
    btn = await qrcode_options_btn()
    await message.answer("Select QR option:", reply_markup=btn)
    await UserStates.select_qr_option.set()


async def qrcode_options_state(message: Message, state: FSMContext):
    text = message.text
    if text == '🔙 Back':
        await state.reset_state(with_data=False)
        return await start_bot_handler(message)

    await state.update_data(qrcode_options=text, scale=8, dark_color="#000", light_color="#fff")
    if text in qr_option_btn_names:

        btn = await cancel_btn()
        context = await is_equal_option(text)
        await message.answer(context, reply_markup=btn)
        await UserStates.get_text.set()
    elif text in qr_media_option_btn_names:
        btn = await cancel_btn()
        context = "Enter your text:"
        await message.answer(context, reply_markup=btn)
        await UserStates.get_media_text.set()


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


async def get_qrcode_get_media_text_state(message: Message, state: FSMContext):
    text = message.text
    data = await state.get_data()
    if text in ['❌ Cancel', '/start']:
        await state.finish()
        return await start_bot_handler(message)

    await state.update_data(text=text)
    context = await is_equal_option(data['qrcode_options'])
    await message.answer(context)
    await UserStates.get_media.set()


async def get_qrcode_media_state(message: Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text
    if text in ['❌ Cancel', '/start']:
        await state.finish()
        return await start_bot_handler(message)

    data = await state.get_data()
    if message.content_type == 'photo':
        await message.photo[-1].download(destination_file=f"qrimg_{user_id}.png")
        filename = await check_qrcode_option(user_id, data['qrcode_options'], data['text'])
        btn = await start_menu_btn()
        await message.answer("👇", reply_markup=btn)

        btn = await qrcode_settings_btn(is_media=True)
        await message.answer_photo(InputFile(filename), reply_markup=btn)

    elif message.content_type == 'animation':
        btn = await start_menu_btn()
        wait_msg = await message.answer("⏳", reply_markup=btn)
        await message.animation.download(destination_file=f"qrgif_{user_id}.mp4")
        await convert_to_gif(user_id)
        filename = await check_qrcode_option(user_id, data['qrcode_options'], data['text'])
        await message.answer_animation(InputFile(filename))
        await wait_msg.delete()
        await delete_medies(user_id)
    else:
        await message.answer("It`s not Image or Gif")

    await state.reset_state(with_data=False)


async def qrcode_setting_scale_callback(c: CallbackQuery, state: FSMContext):
    user_id = c.from_user.id
    data = await state.get_data()
    scale_options = data['scale'] + 2 if c.data.split(":")[-1] == 'plus' else data['scale'] - 2
    await state.update_data(scale=scale_options)
    if data['qrcode_options'] in qr_media_option_btn_names:
        filename = await check_qrcode_option(user_id, data['qrcode_options'], data['text'], scale=scale_options)
        btn = await qrcode_settings_btn(is_media=True)
    else:
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
    await delete_medies(user_id)


async def check_invited_user_callback(c: CallbackQuery):
    user_id = c.from_user.id
    channels = await get_all_channels()
    is_invited = await check_invite(user_id, channels)
    if is_invited:
        await c.message.delete()
        await start_bot_handler(c.message)
    else:
        await c.answer("❗️ You don't subscribe", show_alert=True)


def register_users_py(dp: Dispatcher):
    dp.register_message_handler(start_bot_handler, commands=['start'])

    dp.register_message_handler(start_bot_handler, text="🔙 Back")
    dp.register_message_handler(info_handler, text="ℹ️ Info")
    dp.register_message_handler(support_handler, text="👤 Support")
    dp.register_message_handler(qrcode_options_handler, text="✏️ QR Code generation")

    dp.register_message_handler(qrcode_options_state, state=UserStates.select_qr_option, content_types=['text'])
    dp.register_message_handler(get_qrcode_text_state, state=UserStates.get_text, content_types=['text'])
    dp.register_message_handler(get_qrcode_get_media_text_state, state=UserStates.get_media_text,
                                content_types=['text'])
    dp.register_message_handler(get_qrcode_media_state, state=UserStates.get_media,
                                content_types=['animation', 'photo', 'text'])

    dp.register_callback_query_handler(qrcode_finish_callback, text="qr_finish")
    dp.register_callback_query_handler(check_invited_user_callback, text="invited")
    dp.register_callback_query_handler(qrcode_setting_scale_callback, text_contains="scale")
    dp.register_callback_query_handler(qrcode_setting_color_callback, text_contains="color")
