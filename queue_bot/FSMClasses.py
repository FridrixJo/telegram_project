from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMAdmin(StatesGroup):
    choose_user = State()
    numbers_or_back = State()
    choose_phone = State()
    phone_info_back = State()
    admin_opportunities = State()
    cancel = State()
    user = State()
    days = State()
    period_list = State()
    del_param = State()
    sharing = State()
    sharing_start = State()
    sharing_using = State()
    statistics = State()
    del_list = State()
    condition = State()

    choose_user_WS = State()
    WS_numbers_or_back = State()
    WS_back = State()


class FSMSubAdmin(StatesGroup):
    sub_admin_opps = State()
    input_user = State()
    sub_days = State()
    sub_cancel = State()
    sharing = State()


class FSMWebScraper(StatesGroup):
    ListNumbers = State()
    opportunities = State()
    last_chance = State()
    number = State()
    password = State()
    choice = State()
    chat = State()
    minutes = State()
    is_premium = State()
    mailing_text = State()
    telegram_code = State()
