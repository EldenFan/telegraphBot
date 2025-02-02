from aiogram.fsm.state import StatesGroup, State

class CopyTelegraphStates(StatesGroup):
    waiting_for_author = State()