import asyncio
import random
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart,Command
from aiogram .types import Message
from config import TOKEN, LIST


bot=Bot(token=TOKEN)
dp=Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет! Я бот")

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды:\n/start\n/help")
@dp.message(F.text == "что такое ИИ?")
async def aitext(message: Message):
    await message.answer('Искусственный интеллект — это свойство искусственных интеллектуальных систем выполнять творческие функции, которые традиционно считаются прерогативой человека; наука и технология создания интеллектуальных машин, особенно интеллектуальных компьютерных программ')


@dp.message(F.photo)
async def react_photo(message: Message):
    list = ["Ого, какая фотка!", "Непонятно, что это такое", "Не отправляй мне такое больше"]
    rand_answ = random.choice(list)
    await message.answer(rand_answ)
@dp.message(Command('photo'))
async def photo(message: Message):
    # list = [ссылки URL на изображения через запятую]
    rand_photo = random.choice(LIST)
    await message.answer_photo(photo=rand_photo, caption='Это супер крутая картинка')

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

