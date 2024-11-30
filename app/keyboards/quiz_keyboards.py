from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def get_keyboard_introduction() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Нет, но я бы очень хотел это узнать!", callback_data='start_quiz')]
    ])

def get_keyboard_start_quiz() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard = [[KeyboardButton(text="📝 Заполнить анкету")]],
        resize_keyboard=True
    )

def get_keyboard_answers() -> ReplyKeyboardMarkup:
    kb_list = [[
        KeyboardButton(text="1"),
        KeyboardButton(text="2"),
        KeyboardButton(text="3"),
        KeyboardButton(text="4"),
    ]]
    return ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True)

def get_keyboard_finish_quiz() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Показать результат")]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def get_keyboard_links(animal_name, image_link, description_link) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=f'{animal_name}',
            url=f'{description_link}'
        )],
        [InlineKeyboardButton(
            text="Поделиться в ВК",
            url=f'https://vk.com/share.php?url=http://t.me/moscow_zooBot&image={image_link}&'
                f'title=Мое тотемное животное {animal_name}'
        )]
    ])

def get_keyboard_more_details() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Расскажи подробнее...', callback_data='guardianship_program')]
    ])

def get_keyboard_guardianship_program() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Клуб друзей', url='https://moscowzoo.siteindev.ru/about/'),
            InlineKeyboardButton(text='Программа опеки', url='https://moscowzoo.ru/about/guardianship')
        ]
    ])

def get_keyboard_restart_quiz() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text='📝 Повторить анкету')]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
