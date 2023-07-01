import os

import segno
from PIL import Image
from segno import helpers
from qrcode_artistic import write_artistic
from moviepy.editor import VideoFileClip
import imageio


qr_option_btn_names = ['🔹 Simple [QR]', '🔹 Wifi [QR]', '🔹 Location [QR]', '🔹 Contact [QR]']
qr_media_option_btn_names = ['🔹 Picture [QR]', '🔹 Gif [QR]']


async def delete_medies(user_id):
    try:
        os.unlink(f"qr_{user_id}.png")
    except:
        pass
    try:
        os.unlink(f"qrgif_{user_id}.mp4")
    except:
        pass
    try:
        os.unlink(f"qrimg_{user_id}.png")
    except:
        pass


async def convert_to_gif(user_id):
    video_clip = VideoFileClip(f"qrgif_{user_id}.mp4", verbose=False)
    frames = [frame for frame in video_clip.iter_frames()]
    imageio.mimsave(f"qrgif_{user_id}.gif", frames)


async def spliting_by_option(option, text):
    if option == "🔹 Simple [QR]":
        return text
    elif option == "🔹 Wifi [QR]":
        spl = text.split("\n")
        if len(spl) == 3:
            return {
                "ssid": spl[0],
                "password": spl[1],
                "security": spl[2],
            }
        else:
            return False
    elif option == "🔹 Location [QR]":
        spl = text.split("\n")
        if len(spl) == 2:
            try:
                return [float(spl[0]), float(spl[1])]
            except:
                return False
        else:
            return False
    elif option == "🔹 Contact [QR]":
        spl = text.split("\n")
        if len(spl) == 2:
            return {
                "name": spl[0],
                "phone": spl[1],
            }
        else:
            return False
    elif option == "🔹 Picture [QR]":
        return ""
    elif option == "🔹 Gif [QR]":
        return ""


async def is_equal_option(text):
    if text == "🔹 Simple [QR]":
        return "Enter your text:"
    elif text == "🔹 Wifi [QR]":
        return "Enter your wifi info.\n\n" \
               "<em>Example:</em>\n" \
               "<code>mywifi</code>\n" \
               "<code>123</code>\n" \
               "<code>WPA</code>"
    elif text == "🔹 Location [QR]":
        return "Enter your location (lat, lng).\n\n" \
               "<em>Example:</em>\n" \
               "<code>38.6846841</code>\n" \
               "<code>-77.4521486</code>"
    elif text == "🔹 Contact [QR]":
        return "Enter your contact info.\n\n" \
               "<em>Example:</em>\n" \
               "<code>John</code>\n" \
               "<code>+1 234 567 89 45</code>"

    elif text == "🔹 Picture [QR]":
        return "Send Image"
    elif text == "🔹 Gif [QR]":
        return "Send Gif"


async def check_qrcode_option(user_id, option, text, dark_color="#000", light_color="#fff", scale=8):
    if option == "🔹 Simple [QR]":
        return await make_simple_qrcode(user_id, text, dark_color, light_color, scale)
    elif option == "🔹 Wifi [QR]":
        return await make_wifi_qrcode(user_id, text, dark_color, light_color, scale)
    elif option == "🔹 Location [QR]":
        return await make_location_qrcode(user_id, text, dark_color, light_color, scale)
    elif option == "🔹 Contact [QR]":
        return await make_personal_qrcode(user_id, text, dark_color, light_color, scale)
    elif option == "🔹 Picture [QR]":
        return await make_pic_qrcode(user_id, text, scale)
    elif option == "🔹 Gif [QR]":
        return await make_gif_qrcode(user_id, text, scale)


async def make_simple_qrcode(user_id, text, dark_color="#000", light_color="#fff", scale=8):
    filename = f"qr_{user_id}.png"
    qrcode = segno.make(text)
    qrcode.save(filename, scale=scale, dark=dark_color, light=light_color)
    return filename


async def make_wifi_qrcode(user_id, text, dark_color="#000", light_color="#fff", scale=8):
    filename = f"qr_{user_id}.png"
    wifi = helpers.make_wifi(**text)
    wifi.save(filename, scale=scale, dark=dark_color, light=light_color)
    return filename


async def make_location_qrcode(user_id, text, dark_color="#000", light_color="#fff", scale=8):
    filename = f"qr_{user_id}.png"
    qr_geo = helpers.make_geo(lat=text[0], lng=text[1])
    qr_geo.save(filename, scale=scale, dark=dark_color, light=light_color)
    return filename


async def make_personal_qrcode(user_id, text, dark_color="#000", light_color="#fff", scale=8):
    filename = f"qr_{user_id}.png"
    qr_contact = helpers.make_mecard(**text)
    qr_contact.save(filename, scale=scale, dark=dark_color, light=light_color)
    return filename


async def make_pic_qrcode(user_id, text, scale=8):
    filename = f"qr_{user_id}.png"
    background = f"qrimg_{user_id}.png"
    qrcode_img = segno.make(text, error="h")
    write_artistic(qrcode_img, background=background, target=filename, scale=scale)
    return filename


async def make_gif_qrcode(user_id, text, scale=8):
    filename = f"qr_{user_id}.gif"
    background = f"qrgif_{user_id}.gif"
    qrcode_gif = segno.make(text, error="h")
    write_artistic(qrcode_gif, background=background, target=filename, scale=scale)
    return filename
