from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile
from app import bot
from app.keyboards.quiz_keyboards import get_keyboard_links, get_keyboard_more_details
from app.db.db_requests import DataBase
from app.states.quiz_states import QuizStates

finish_quiz_router = Router()

@finish_quiz_router.message(QuizStates.finish_quiz)
async def quiz_finish_handler(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    counter_answers = data['counter_answers']

    counter_answers = dict(sorted(counter_answers.items(), key=lambda item: item[1], reverse=True))
    answers_max_to_min = tuple(counter_answers.keys())

    answers_max_to_min = ''.join(answers_max_to_min)

    db = DataBase()
    animal_id, answers, animal_name, image_path, image_link, description_link = db.get_animals_data(answers_max_to_min)[0]
    photo = FSInputFile(image_path)
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=photo,
        reply_markup=get_keyboard_links(animal_name, image_link, description_link),
        caption=f'Твое тотемное животное - {animal_name}'
    )

    await state.update_data(animal_name=animal_name)

    await message.answer('Теперь у тебя есть возможность помочь Московскому зоопарку и поделиться своей '
                         'силой и заботой - это прекрасная возможность принять участие в деле сохранения редких видов, '
                         'помочь нам в реализации природоохранных программ.', reply_markup=get_keyboard_more_details())
    await state.set_state(QuizStates.guardianship_program)

