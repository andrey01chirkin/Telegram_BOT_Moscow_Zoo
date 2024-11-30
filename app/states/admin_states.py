from aiogram.fsm.state import StatesGroup, State

class AdminStates(StatesGroup):
    insert_question = State()
    insert_answers = State()
    choose_question_for_changing = State()
    input_new_question = State()
    choose_question_for_deleting = State()
    choose_question = State()
    choose_answer = State()
    input_new_answer = State()
    replace_new_answer = State()