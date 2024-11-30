from .finish_quiz import finish_quiz_router
from .guardianship_program import guardianship_program_router
from .quiz import input_data_quiz_router
from .start_quiz import quiz_router, start_quiz_router

quiz_router.include_routers(
    start_quiz_router,
    input_data_quiz_router,
    finish_quiz_router,
    guardianship_program_router
)