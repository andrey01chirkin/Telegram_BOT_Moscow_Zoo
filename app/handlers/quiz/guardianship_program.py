from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.keyboards.quiz_keyboards import get_keyboard_guardianship_program, get_keyboard_restart_quiz
from app.states.quiz_states import QuizStates

guardianship_program_router = Router()

@guardianship_program_router.callback_query(QuizStates.guardianship_program, F.data == 'guardianship_program')
async def show_more_details_handler(callback:CallbackQuery, state: FSMContext):
    await callback.message.answer('В рамках Программы лояльности Московского зоопарка любой желающий может взять одно из '
                                  'животных под свою опеку. Все - от маленьких посетителей до больших корпораций, - кто '
                                  'неравнодушен к жизни обитателей зоопарка, '
                                  'может стать участником программы.', reply_markup=get_keyboard_guardianship_program())
    await state.set_state(QuizStates.quiz)
    await callback.message.answer(
        'Если Вас заинтересовала программа опеки, Вы можете связаться с нами напрямую,'
        'используя команду /connect\n\n<b>До встречи!</b>', reply_markup=get_keyboard_restart_quiz()
    )


