import asyncio
import logging
import sys
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from app import bot
from app.handlers.admin.start_admin import admin_router
from app.handlers.connect.connect import connect_router
from app.handlers.feedback.feedback import feedback_router
from app.handlers.incorrect_data.incorrect_data import final_router
from app.handlers.quiz import quiz_router

async def main() -> None:
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers (
        quiz_router,
        connect_router,
        feedback_router,
        admin_router,
        final_router
    )
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format="%(asctime)s %(levelname)s %(message)s"
    )
    asyncio.run(main())