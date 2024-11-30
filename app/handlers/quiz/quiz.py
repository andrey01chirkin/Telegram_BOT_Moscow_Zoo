import emoji
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from app.db.db_requests import DataBase
from app.keyboards.quiz_keyboards import get_keyboard_finish_quiz, get_keyboard_answers
from app.states.quiz_states import QuizStates

input_data_quiz_router = Router()

@input_data_quiz_router.message(QuizStates.quiz, F.text.in_(['1', '2', '3', '4', '📝 Заполнить анкету', '📝 Повторить анкету']))
async def quiz_handler(message: Message, state: FSMContext):
    if message.text in ('📝 Заполнить анкету', '📝 Повторить анкету'):
        db = DataBase()
        questions_answers = db.get_questions_answers()  # получает вопросы и ответы из бд
        await state.update_data(question_index=0)
        await state.update_data(questions_answers=questions_answers)  # записываем в хранилище вопросы и ответы
        await state.update_data(amount_questions=len(questions_answers))  # записываем в хранилище кол-во вопросов
        await state.update_data(counter_answers={'1': 0, '2': 0, '3': 0, '4': 0})

    data = await state.get_data()

    counter_answers = data['counter_answers']
    if message.text in counter_answers:
        counter_answers[message.text] += 1
        await state.update_data(counter_answers=counter_answers)

    if data['question_index'] == data['amount_questions']:
        await state.set_state(QuizStates.finish_quiz)
        await message.answer(
            f'Викторина окончена {emoji.emojize(':party_popper:')}',
            reply_markup=get_keyboard_finish_quiz()
        )
        return

    question_index = data['question_index']
    question = data['questions_answers'][question_index][1]
    answers = data['questions_answers'][question_index][2].split(';')

    await state.update_data(question_index=question_index + 1)

    await message.answer(
        f'<b>{question}</b>\n'
        f'1. {answers[0]}\n'
        f'2. {answers[1]}\n'
        f'3. {answers[2]}\n'
        f'4. {answers[3]}\n',
        reply_markup=get_keyboard_answers()
    )
