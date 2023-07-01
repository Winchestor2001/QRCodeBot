from playhouse.shortcuts import model_to_dict

from data.config import ADMINS
from .models import *


async def add_user(user_id: int, username: str):
    with db:
        if not Users.select().where(Users.user_id == user_id).exists():
            Users.create(user_id=user_id, username=username)


async def get_all_users():
    with db:
        return Users.select().count()


async def save_channel(channel_id, channel_name, channel_url):
    with db:
        if not Channels.select().where(Channels.channel_id == channel_id).exists():
            Channels.create(channel_id=channel_id, channel_name=channel_name, channel_url=channel_url)


async def get_all_channels():
    with db:
        return [model_to_dict(item) for item in Channels.select()]


async def del_channel(channel_id):
    with db:
        Channels.delete().where(Channels.channel_id == channel_id).execute()

