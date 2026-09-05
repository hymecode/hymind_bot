from aiogram import Dispatcher

def setup_handlers(dp: Dispatcher):
    # Har bir bo'limni shu yerga qo'shing
    from .start import router as start_router
    from .translate import router as translate_router
    # from .pomodoro import router as pomodoro_router  # KEYIN QO'SHASIZ
    # from .premium import router as premium_router    # KEYIN QO'SHASIZ
    # from .promo import router as promo_router        # KEYIN QO'SHASIZ
    # from .profile import router as profile_router    # KEYIN QO'SHASIZ
    
    dp.include_router(start_router)
    dp.include_router(translate_router)
    # dp.include_router(pomodoro_router)  # KEYIN QO'SHASIZ
    # dp.include_router(premium_router)   # KEYIN QO'SHASIZ
    # dp.include_router(promo_router)     # KEYIN QO'SHASIZ
    # dp.include_router(profile_router)   # KEYIN QO'SHASIZ