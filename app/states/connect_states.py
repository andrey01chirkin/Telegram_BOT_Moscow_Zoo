from aiogram.fsm.state import StatesGroup, State

class ConnectStates(StatesGroup):
    name = State()
    phone = State()
    email = State()
    content = State()