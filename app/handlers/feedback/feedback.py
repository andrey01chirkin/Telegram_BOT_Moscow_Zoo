import os
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from app import bot
from app.db.db_requests import DataBase
from app.states.feedback_states import FeedbackStates
from config import admin_list

feedback_router = Router()

@feedback_router.message(F.text, Command('feedback'))
async def command_connect_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer('Введите Ваше имя')
    await state.set_state(FeedbackStates.name_user)

@feedback_router.message(FeedbackStates.name_user, F.text, ~F.text.startswith('/'))
async def input_name_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(FeedbackStates.content_data)
    await message.answer('Введите Ваш отзыв')

@feedback_router.message(FeedbackStates.content_data, F.text, ~F.text.startswith('/'))
async def input_content_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(content=message.text)
    data = await state.get_data()
    db = DataBase()
    db.insert_feedback_data(data)
    if message.from_user.id not in admin_list:
        await bot.send_message(chat_id=os.getenv('CHAT_ID'), text=f'Пользователь {data['name']} оставил отзыв')
    await message.answer('Благодарим за обратную связь!')
    await state.clear()



