from aiogram.fsm.state import StatesGroup, State

class FeedbackStates(StatesGroup):
    name_user = State()
    content_data = State()