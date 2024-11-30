from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from app.handlers.admin import admin_router
from app.keyboards.admin_keyboards import get_keyboard_admin
from config import admin_list


@admin_router.message(F.text, Command('admin'))
async def command_admin_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    if message.from_user.id in admin_list:
        await message.answer('Выберите действие', reply_markup=get_keyboard_admin())
    else:
        await message.answer('Вы не являетесь администратором')


