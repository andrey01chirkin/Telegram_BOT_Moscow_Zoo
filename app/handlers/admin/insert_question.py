from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from app.db.db_requests import DataBase
from app.handlers.admin.IsAdmin import IsAdmin
from app.states.admin_states import AdminStates
from config import admin_list

admin_insert_question_answers = Router()

@admin_insert_question_answers.message(F.text == 'Вставить вопрос', IsAdmin(admin_list))
async def insert_question_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(AdminStates.insert_question)
    await message.answer('Напишите вопрос для вставки')

@admin_insert_question_answers.message(AdminStates.insert_question, F.text, IsAdmin(admin_list))
async def insert_question_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(question = message.text)
    await state.set_state(AdminStates.insert_answers)
    await message.answer('<b>Введите ответы в формате:</b>\nответ1;\nответ2;\nответ3;\nответ4')

@admin_insert_question_answers.message(AdminStates.insert_answers, F.text, IsAdmin(admin_list))
async def insert_question_handler(message: Message, state: FSMContext) -> None:
    source_line = message.text
    if source_line.count(';') == 3:
        answers = source_line.replace('\n', '').split(';')
        answers = [line.strip() for line in answers]
        await state.update_data(answers=answers)
        data = await state.get_data()
        db = DataBase()
        status = db.insert_questions_answers(data)
        if status:
            await message.answer('Вопрос и 4 ответа записаны в БД')
        else:
            await message.answer('Вопрос уже существует\nЧтобы открыть админ панель нажмите /admin')
        await state.clear()
    else:
        await message.answer('<b>Данные не соответствуют формату</b>\nВведите ответы в формате:\nответ1;\nответ2;\nответ3;\nответ4')
        return
