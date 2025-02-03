from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from config import TOKEN, TELEGRAPH_URL_PATTERN
import asyncio
import re
from telegraphCopy import copy_telegraph
from states import CopyTelegraphStates

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer("Отправьте ссылку на telegraph статью")


@dp.message(CopyTelegraphStates.waiting_for_author)
async def telegraph_url(message: Message, state: FSMContext) -> None:
    await message.answer("Копирую статью, подождите...")
    data = await state.get_data()
    url = data.get("url")
    title = data.get("title")
    new_url = await copy_telegraph(url=url, title=title, author=message.text)
    await message.answer(new_url)
    await state.clear()


@dp.message(CopyTelegraphStates.waiting_for_title)
async def get_author(message: Message, state: FSMContext) -> None:
    await message.answer("Введите автора: ")
    await state.update_data(title = message.text)
    await state.set_state(CopyTelegraphStates.waiting_for_author)


@dp.message(F.text.contains("https://telegra.ph/"))
async def telegraph_handler(message: Message, state: FSMContext) -> None:
    await message.answer("Вы отправили telegraph статью")
    match = re.search(TELEGRAPH_URL_PATTERN, message.text)
    if not match:
        await message.answer("Так не должно быть. Обратись в поддержку")
        return
    url = match.group(0)
    get_title(message, url, state)
    

@dp.message(F.content_type == "text")
async def url_handler(message: Message, state: FSMContext) -> None:
    entities = message.entities
    if entities:
        for entity in entities:
            url = entity.url
            await get_title(message, url, state)
    else:
        all_handler(message)


@dp.message()
async def all_handler(message: Message) -> None:
    await message.answer("Я не знаю, что с этим делать. Отправте ссылка на telegraph статью. Она должна содержать https://telegra.ph/")


async def get_title(message: Message, url: str, state: FSMContext) -> None:
    await message.answer("Введите название:")
    await state.update_data(url = url)
    await state.set_state(CopyTelegraphStates.waiting_for_title)


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())