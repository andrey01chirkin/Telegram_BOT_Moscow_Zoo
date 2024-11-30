import os
import re
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from app import bot
from app.db.db_requests import DataBase
from app.states.connect_states import ConnectStates
from config import admin_list

connect_router = Router()

@connect_router.message(F.text, Command('connect'))
async def command_connect_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer('Введите Ваше имя')
    await state.set_state(ConnectStates.name)

@connect_router.message(ConnectStates.name, F.text, ~F.text.startswith('/'), ~F.text.startswith('📝 Повторить анкету'))
async def input_name_handler(message: Message, state: FSMContext) -> None:
    name = message.text
    await state.update_data(name=name)
    await state.set_state(ConnectStates.phone)
    await message.answer('Введите номер телефона в формате\n+7(xxx)xxx-xx-xx')

@connect_router.message(ConnectStates.phone, F.text, ~F.text.startswith('/'))
async def input_phone_handler(message: Message, state: FSMContext) -> None:
    phone = message.text
    pattern = r'^\+7\(\d{3}\)\d{3}-\d{2}-\d{2}$'
    if re.match(pattern, phone):
        await state.update_data(phone=phone)
    else:
        await message.answer('Телефон не соответствует формату\n+7(xxx)xxx-xx-xx')
        await message.answer('Введите телефон повторно')
        return
    await state.set_state(ConnectStates.email)
    await message.answer('Введите email')

@connect_router.message(ConnectStates.email, F.text, ~F.text.startswith('/'))
async def input_email_handler(message: Message, state: FSMContext) -> None:
    email = message.text
    pattern = re.compile(r"^\S+@\S+\.\S+$")
    if re.match(pattern, email):
        await state.update_data(email=email)
    else:
        await message.answer('Email не соответствует формату')
        await message.answer('Введите email повторно')
        return
    await state.set_state(ConnectStates.content)
    await message.answer('Введите ваш вопрос')

@connect_router.message(ConnectStates.content, F.text, ~F.text.startswith('/'))
async def input_email_handler(message: Message, state: FSMContext) -> None:
    content = message.text
    await state.update_data(content=content)
    data = await state.get_data()
    db = DataBase()
    db.insert_application(data)
    if message.from_user.id not in admin_list:
        await bot.send_message(chat_id=os.getenv('CHAT_ID'), text=f'Пользователь {data['name']} оставил заявку')
    await message.answer('Сотрудник свяжется с Вами в течении часа')
    await state.clear()

