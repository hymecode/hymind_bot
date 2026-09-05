from aiogram import Dispatcher

def setup_handlers(dp: Dispatcher):
    from .start import router as start_router
    from .translate import router as translate_router
    from .premium import router as premium_router
    from .promo import router as promo_router  # YANGI

    dp.include_router(start_router)
    dp.include_router(translate_router)
    dp.include_router(premium_router)
    dp.include_router(promo_router)  # YANGI