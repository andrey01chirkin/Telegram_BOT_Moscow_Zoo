from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from app.db.db_requests import DataBase
from app.handlers.admin.IsAdmin import IsAdmin
from app.states.admin_states import AdminStates
from config import admin_list

admin_delete_question = Router()

@admin_delete_question.message(F.text == 'Удалить вопрос', IsAdmin(admin_list))
async def delete_question_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    db = DataBase()
    all_questions = db.get_all_questions()
    await state.update_data(amount_questions=len(all_questions))
    await state.update_data(all_questions=all_questions)
    all_questions_string = '<b>Вопросы в БД:</b>\n'
    for index, line in enumerate(all_questions):
        all_questions_string += f'<b>{index + 1}.</b> {line[1]}\n'
    await message.answer(all_questions_string)
    await message.answer('Введите номер вопроса для удаления')
    await state.set_state(AdminStates.choose_question_for_deleting)

@admin_delete_question.message(F.text, AdminStates.choose_question_for_deleting, IsAdmin(admin_list))
async def delete_question_handler(message: Message, state: FSMContext) -> None:
    try:
        number_question = int(message.text)
        data = await state.get_data()
        if 1 <= number_question <= data['amount_questions']:
            index_question_for_deleting = number_question - 1
            question_id = data['all_questions'][index_question_for_deleting][0]
            db = DataBase()
            db.delete_question_answers(question_id)
            await message.answer(f'Вопрос под номеров {number_question} удален.\nТакже удалены ответы для данного вопроса')
            await state.clear()
        else:
            raise ValueError
    except ValueError:
        await message.answer('Некорректный номер вопроса\nНомер должен быть числом\nПопробуйте еще раз')
        return



