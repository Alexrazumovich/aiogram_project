import asyncio,requests
import random
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart,Command
from aiogram .types import Message,FSInputFile
from config import TOKEN, WEATHER_API_KEY
from gtts import gTTS
from googletrans import Translator
import os,sqlite3
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import aiohttp
import logging

bot=Bot(token=TOKEN)
dp=Dispatcher()

logging.basicConfig(level=logging.INFO)

class Form(StatesGroup):
    name=State()
    age=State()
    city=State()
def init_db():
	conn = sqlite3.connect('user_data.db')
	cur = conn.cursor()
	cur.execute('''
	CREATE TABLE IF NOT EXISTS users (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL,
	age INTEGER NOT NULL,
	city TEXT NOT NULL)
	''')
	conn.commit()
	conn.close()

init_db()

@dp.message(CommandStart())
async def start(message: Message,state:FSMContext):
    await message.answer("Привет! Как тебя зовут?")
    await state.set_state(Form.name)
@dp.message(Form.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько тебе лет?")
    await state.set_state(Form.age)
@dp.message(Form.age)
async def age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("Из какого ты города?")
    await state.set_state(Form.city)
@dp.message(Form.city)
async def city(message: Message, state:FSMContext):
    await state.update_data(city=message.text)
    user_data = await state.get_data()
    print(user_data['name'])
    conn = sqlite3.connect('user_data.db')
    cur = conn.cursor()
    cur.execute('''INSERT INTO users (name, age, city) VALUES (?,?,?)''', (user_data['name'], user_data['age'], user_data['city']))
    conn.commit()
    conn.close()
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.openweathermap.org/data/2.5/weather?q={user_data["city"]}&appid={WEATHER_API_KEY}&units=metric') as response:
            if response.status == 200:
                weather_data = await response.json()
                main = weather_data['main']
                weather = weather_data['weather'][0]
                temperature = main['temp']
                humidity = main['humidity']
                description = weather['description']
                weather_report = (f"Город - {user_data['city']}\n"
                                  f"Температура - {temperature}\n"
                                  f"Влажность воздуха - {humidity}\n"
                                  f"Описание погоды - {description}")
                await message.answer(weather_report)
            else:
                await message.answer("Произошла ошибка при получении информации о погоде.")
    await state.clear()





async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())