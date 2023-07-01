from loader import bot


async def check_invite(user_id, channels):
    for channel in channels:
        user_status = await bot.get_chat_member(channel['channel_id'], user_id)
        if user_status.status == "left":
            return False

    return True
