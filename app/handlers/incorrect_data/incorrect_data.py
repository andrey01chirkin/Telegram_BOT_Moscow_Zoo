from aiogram import Router
from aiogram.types import Message

final_router = Router()

@final_router.message()
async def text_handler(message: Message) -> None:
    await message.answer('<b>Доступные команды:</b>\n'
                         '/start - запустить бота\n'
                         '/connect - связаться с сотрудником зоопарка\n'
                         '/feedback - оставить обратную связь\n'
                         '/admin - админ панель')