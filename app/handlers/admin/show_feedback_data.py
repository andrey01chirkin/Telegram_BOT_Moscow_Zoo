from aiogram import Router, F
from aiogram.types import Message
from app.db.db_requests import DataBase
from app.handlers.admin.IsAdmin import IsAdmin
from config import admin_list

admin_show_feedback_data = Router()

@admin_show_feedback_data.message(F.text == 'Обратная связь', IsAdmin(admin_list))
async def show_feedback_data_handler(message: Message) -> None:
    db = DataBase()
    feedback_data = db.get_feedback_data()
    feedback_data_string = ''
    for line in feedback_data:
        feedback_data_string += (f'<b>Имя пользователя:</b> {line[1]}\n'
                                f'<b>Обратная связь от пользователя:</b>\n{line[2]}\n\n')
    await message.answer(feedback_data_string)


