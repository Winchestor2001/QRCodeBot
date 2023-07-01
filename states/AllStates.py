from aiogram.dispatcher.filters.state import StatesGroup, State


class UserStates(StatesGroup):
    get_text = State()
    get_media = State()
    get_media_text = State()

    select_qr_option = State()


