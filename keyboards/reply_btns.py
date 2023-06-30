from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


async def start_menu_btn():
    btn = ReplyKeyboardMarkup(resize_keyboard=True)
    btn.row("✏️ QR Code generation")
    btn.row("ℹ️ Info", "👤 Support")

    return btn


async def qrcode_options_btn():
    btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn.add(
        KeyboardButton("🔹 Simple [QR]"),
        KeyboardButton("🔹 Wifi [QR]"),
        KeyboardButton("🔹 Location [QR]"),
        KeyboardButton("🔹 Contact [QR]"),
        KeyboardButton("🔹 Picture [QR]"),
        KeyboardButton("🔹 Gif [QR]"),
        KeyboardButton("🔙 Back"),
    )

    return btn


async def cancel_btn():
    btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn.add(
        KeyboardButton("❌ Cancel")
    )
    return btn

