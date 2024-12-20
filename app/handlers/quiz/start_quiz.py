from aiogram import html, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, CallbackQuery, ReplyKeyboardRemove
from app import bot
from app.keyboards.quiz_keyboards import get_keyboard_introduction, get_keyboard_start_quiz
from aiogram import F
from app.states.quiz_states import QuizStates

start_quiz_router = Router()
quiz_router = Router()

@start_quiz_router.message(F.text, CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(QuizStates.start_quiz)
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=FSInputFile('data/images/animals/panda_katyusha.jpeg'),
        caption=f"Привет, <b>{html.bold(message.from_user.full_name)}!</b>\n"
                f"Я Катюша, символ и гордость Московского зоопарка. \nЯ очень рада тебя видеть!\n"
                f"Твой внутренний зверь так и рвется на волю!\n"
                f"Ты знаешь кто он?",
        reply_markup=get_keyboard_introduction()
    )

@start_quiz_router.message(QuizStates.start_quiz, F.text == 'Нет, но я бы очень хотел это узнать!')
async def start_quiz_handler(message: Message, state: FSMContext):
    photo = FSInputFile('data/images/logo/MZoo-logo-сircle-universal-preview.jpg')
    await state.set_state(QuizStates.quiz)
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=photo,
        caption="<b>Заполни анкету, чтобы узнать какое животное из московского зоопарка тебе близко по духу</b>",
        reply_markup=get_keyboard_start_quiz()
    )
