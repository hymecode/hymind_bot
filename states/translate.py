from aiogram.fsm.state import State, StatesGroup

class TranslateState(StatesGroup):
    waiting_text = State()