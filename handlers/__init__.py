# handlers/__init__.py

from aiogram import Dispatcher

def setup_handlers(dp: Dispatcher):
    from .start import router as start_router
    from .translate import router as translate_router
    from .tests import router as tests_router
    from .support import router as support_router
    from .media import router as media_router

    dp.include_router(start_router)
    dp.include_router(translate_router)
    dp.include_router(tests_router)
    dp.include_router(support_router)
    dp.include_router(media_router)