from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from app.handlers.admin.IsAdmin import IsAdmin
from app.states.admin_states import AdminStates
from app.db.db_requests import DataBase
from config import admin_list

admin_change_answers = Router()

@admin_change_answers.message(F.text == 'Изменить ответ на вопрос', IsAdmin(admin_list))
async def change_answers_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    db = DataBase()
    all_questions = db.get_all_questions()
    await state.update_data(amount_questions=len(all_questions))
    await state.update_data(all_questions=all_questions)
    all_questions_string = '<b>Вопросы в БД:</b>\n'
    for index, line in enumerate(all_questions):
        all_questions_string += f'<b>{index + 1}.</b> {line[1]}\n'
    await message.answer(all_questions_string)
    await message.answer('Введите номер вопроса для изменения ответов')
    await state.set_state(AdminStates.choose_question)

@admin_change_answers.message(F.text, AdminStates.choose_question, IsAdmin(admin_list))
async def change_answers_handler(message: Message, state: FSMContext) -> None:
    try:
        number_question = int(message.text)
        data = await state.get_data()
        if 1 <= number_question <= data['amount_questions']:
            index_question = number_question-1
            question_id = data['all_questions'][index_question][0]
            db = DataBase()
            answers = db.get_answers_by_id(question_id)
            await state.update_data(amount_answers=len(answers))
            await state.update_data(answers=answers)
            answers_string = f'Ответы к вопросу: \n<b>{data['all_questions'][index_question][1]}</b>\n'
            for index, answer in enumerate(answers):
                answers_string += f'<b>{index + 1}.</b> {answer[1]}\n'
            await message.answer(answers_string)
            await message.answer('Введите номер ответа для изменения')
            await state.set_state(AdminStates.input_new_answer)
        else:
            raise ValueError
    except ValueError:
        await message.answer('Некорректный номер вопроса\nНомер должен быть числом\nПопробуйте еще раз')
        return

@admin_change_answers.message(F.text, AdminStates.input_new_answer, IsAdmin(admin_list))
async def change_answers_handler(message: Message, state: FSMContext) -> None:
    try:
        number_answer = int(message.text)
        data = await state.get_data()
        if 1 <= number_answer <= data['amount_answers']:
            index_answer = number_answer-1
            answer_id = data['answers'][index_answer][0]
            await state.update_data(answer_id=answer_id)
            await message.answer('Введите новый ответ для замены:\n')
            await state.set_state(AdminStates.replace_new_answer)
        else:
            raise ValueError
    except ValueError:
        await message.answer('Некорректный номер ответа\nНомер должен быть числом\nПопробуйте еще раз')
        return

@admin_change_answers.message(F.text, AdminStates.replace_new_answer, IsAdmin(admin_list))
async def change_answers_handler(message: Message, state: FSMContext) -> None:
    new_answer = message.text
    data = await state.get_data()
    answer_id = data['answer_id']
    db = DataBase()
    db.update_answer(new_answer, answer_id)
    await message.answer('Ответ изменен в БД')
    await state.clear()

