from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def qrcode_settings_btn(is_media=False):
    btn = InlineKeyboardMarkup(row_width=2)
    btn.add(
        InlineKeyboardButton(f"➕ Scale", callback_data="scale:plus"),
        InlineKeyboardButton(f"➖ Scale", callback_data="scale:minus"),
    )
    if not is_media:
        btn.add(
            InlineKeyboardButton(f"🟤", callback_data="color:#5e4a13"),
            InlineKeyboardButton(f"🟣", callback_data="color:#734496"),
            InlineKeyboardButton(f"🔵", callback_data="color:#4638a1"),
            InlineKeyboardButton(f"🟢", callback_data="color:#1dc264"),
            InlineKeyboardButton(f"🟡", callback_data="color:#f2ee11"),
            InlineKeyboardButton(f"🟠", callback_data="color:#de8d23"),
            InlineKeyboardButton(f"🔴", callback_data="color:#cc1023"),
            InlineKeyboardButton(f"⚫️", callback_data="color:#000"),
        )
    btn.add(
        InlineKeyboardButton(f"✅ Finish", callback_data="qr_finish")
    )
    return btn


async def support_btn():
    btn = InlineKeyboardMarkup()
    btn.add(InlineKeyboardButton(f"👤 Administrator", url="t.me/winchestor_dev"))
    return btn


async def admin_panel_btn():
    btn = InlineKeyboardMarkup(row_width=2)
    btn.add(
        InlineKeyboardButton("Channels", callback_data="channels_list"),
        InlineKeyboardButton("Add Channel", callback_data="add_channel"),
        InlineKeyboardButton("Mailing", callback_data="mailing"),
    )
    return btn


async def channels_list_btn(channels):
    btn = InlineKeyboardMarkup(row_width=2)
    btn.add(
        *[InlineKeyboardButton(f"{n} - ❌", callback_data=f"del_channel:{item['channel_id']}") for n, item in enumerate(channels, 1)]
    )
    return btn


async def invite_channel_btn(channels):
    btn = InlineKeyboardMarkup(row_width=1)
    btn.add(
        *[InlineKeyboardButton(f"▫️ {item['channel_name']}", url=f"{item['channel_url']}") for item in channels],
        InlineKeyboardButton("✅ Submit", callback_data="invited")
    )
    return btn

