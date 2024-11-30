from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from app.db.db_requests import DataBase
from app.handlers.admin.IsAdmin import IsAdmin
from app.states.admin_states import AdminStates
from config import admin_list

admin_change_question = Router()

@admin_change_question.message(F.text == 'Изменить вопрос', IsAdmin(admin_list))
async def change_question_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    db = DataBase()
    all_questions = db.get_all_questions()
    await state.update_data(amount_questions=len(all_questions))
    await state.update_data(all_questions=all_questions)
    all_questions_string = '<b>Вопросы в БД:</b>\n'
    for index, line in enumerate(all_questions):
        all_questions_string += f'<b>{index+1}.</b> {line[1]}\n'
    await message.answer(all_questions_string)
    await message.answer('Введите номер вопроса для изменения')
    await state.set_state(AdminStates.choose_question_for_changing)

@admin_change_question.message(F.text, AdminStates.choose_question_for_changing, IsAdmin(admin_list))
async def change_question_handler(message: Message, state: FSMContext) -> None:
    try:
        number_question = int(message.text)
        data = await state.get_data()
        if 1 <= number_question <= data['amount_questions']:
            await state.update_data(index_question_for_changing=number_question-1)
            await message.answer('Введите новый вопрос:')
            await state.set_state(AdminStates.input_new_question)
        else:
            raise ValueError
    except ValueError:
        await message.answer('Некорректный номер вопроса\nНомер должен быть числом\nПопробуйте еще раз')
        return

@admin_change_question.message(F.text, AdminStates.input_new_question, IsAdmin(admin_list))
async def change_question_handler(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    index_question_for_changing = data['index_question_for_changing']
    question_id = data['all_questions'][index_question_for_changing][0]
    new_question = message.text
    db = DataBase()
    db.update_question(new_question, question_id)
    await message.answer('Вопрос обновлен в БД')
    await state.clear()


