from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_keyboard_admin() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Заявки пользователей'), KeyboardButton(text='Обратная связь')],
            [KeyboardButton(text='Вставить вопрос')],
            [KeyboardButton(text='Изменить вопрос')],
            [KeyboardButton(text='Удалить вопрос')],
            [KeyboardButton(text='Изменить ответ на вопрос')],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
