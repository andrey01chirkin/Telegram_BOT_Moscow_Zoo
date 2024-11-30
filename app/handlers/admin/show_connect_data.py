from aiogram import Router, F
from aiogram.types import Message
from app.db.db_requests import DataBase
from app.handlers.admin.IsAdmin import IsAdmin
from config import admin_list

admin_show_connect_data = Router()

@admin_show_connect_data.message(F.text == 'Заявки пользователей', IsAdmin(admin_list))
async def show_connect_data_handler(message: Message) -> None:
    db = DataBase()
    connect_data = db.get_connect_data()
    connect_data_string = ''
    for line in connect_data:
        connect_data_string += (f'<b>Имя пользователя:</b> {line[1]}\n'
                                f'<b>Телефон:</b> {line[2]}\n'
                                f'<b>Почта:</b> {line[3]}\n'
                                f'<b>Содержание заявки:</b>\n{line[4]}\n\n')
    await message.answer(connect_data_string)

