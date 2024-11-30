from aiogram.fsm.state import StatesGroup, State

class QuizStates(StatesGroup):
    start_quiz = State()
    quiz = State()
    finish_quiz = State()
    guardianship_program = State()

