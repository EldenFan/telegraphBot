from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import F

from config import TOKEN, TELEGRAPH_URL_PATTERN
import asyncio
import re
from telegraphCopy import copy_telegraph

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer("Отправьте ссылку на telegraph статью")


@dp.message(F.text.contains("https://telegra.ph/"))
async def telegraph_handler(message: Message) -> None:
    await message.answer("Вы отправили telegraph статью")
    match = re.search(TELEGRAPH_URL_PATTERN, message.text)

    if not match:
        await message.answer("Так не должно быть. Обратись в поддержку")
        return
    
    url = match.group(0)

    await message.answer("Копирую статью, подождите...")

    new_url = await copy_telegraph(url)

    await message.answer(new_url)
    

@dp.message()
async def all_handler(message: Message) -> None:
    await message.answer("Я не знаю, что с этим делать. Отправте ссылка на telegraph статью. Она должна содержать https://telegra.ph/")
    

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())