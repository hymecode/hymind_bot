from aiogram import Dispatcher

def setup_handlers(dp: Dispatcher):
    from .start import router as start_router
    from .translate import router as translate_router
    # from .pomodoro import router as pomodoro_router   # keyin
    # from .premium import router as premium_router     # keyin
    # from .promo import router as promo_router         # keyin
    # from .profile import router as profile_router     # keyin

    dp.include_router(start_router)
    dp.include_router(translate_router)
    # dp.include_router(pomodoro_router)   # keyin
    # dp.include_router(premium_router)    # keyin
    # dp.include_router(promo_router)      # keyin
    # dp.include_router(profile_router)    # keyin