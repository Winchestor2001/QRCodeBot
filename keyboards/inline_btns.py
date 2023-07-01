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

