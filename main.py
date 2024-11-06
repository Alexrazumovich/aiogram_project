import asyncio,requests
import random
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart,Command
from aiogram .types import Message,FSInputFile
from config import TOKEN, LIST
from gtts import gTTS
from googletrans import Translator
import os


bot=Bot(token=TOKEN)
dp=Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Привет! {message.from_user.first_name}")

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды:\n/start\n/help")
@dp.message(F.text == "что такое ИИ?")
async def aitext(message: Message):
    await message.answer('Искусственный интеллект — это свойство искусственных интеллектуальных систем выполнять творческие функции, которые традиционно считаются прерогативой человека; наука и технология создания интеллектуальных машин, особенно интеллектуальных компьютерных программ')
# @dp.message(Command('translate'))
# async def translate(message: Message):


@dp.message(F.photo)
async def react_photo(message: Message):
    list = ["Ого, какая фотка!", "Непонятно, что это такое", "Не отправляй мне такое больше"]
    rand_answ = random.choice(list)
    tts=gTTS(text=rand_answ,lang='ru')
    tts.save("react_photo.ogg")
    voice=FSInputFile("react_photo.ogg")
    await message.answer(rand_answ)
    await bot.download(message.photo[-1],destination=f"img/{message.photo[-1].file_id}.jpg")
    await bot.send_voice(message.chat.id, voice)
    os.remove("react_photo.ogg")
@dp.message(Command('photo'))
async def photo(message: Message):
    # list = [ссылки URL на изображения через запятую]
    rand_photo = random.choice(LIST)
    await message.answer_photo(photo=rand_photo, caption='Это супер крутая картинка')
@dp.message(Command('video'))
async def video(message: Message):
    video=FSInputFile('video.mp4')
    await bot.send_video(message.chat.id, video)
    await bot.send_chat_action(message.chat.id,'upload_video')


@dp.message(Command('audio'))
async def audio(message: Message):
    audio = FSInputFile('audio.mp3')
    await bot.send_audio(message.chat.id, audio)
    await bot.send_chat_action(message.chat.id,'upload_audio')

@dp.message(Command('voice'))
async def voice(message: Message):
    voice = FSInputFile('sample.ogg')
    await bot.send_voice(message.chat.id, voice)

@dp.message(Command('doc'))
async def doc(message: Message):
    doc = FSInputFile('TG02.pdf')
    await bot.send_document(message.chat.id, doc)

@dp.message(Command('training'))
async def training(message: Message):
    training_list = [
        "Тренировка 1:\n1. Скручивания: 3 подхода по 15 повторений\n2. Велосипед: 3 подхода по 20 повторений (каждая сторона)\n3. Планка: 3 подхода по 30 секунд",
        "Тренировка 2:\n1. Подъемы ног: 3 подхода по 15 повторений\n2. Русский твист: 3 подхода по 20 повторений (каждая сторона)\n3. Планка с поднятой ногой: 3 подхода по 20 секунд (каждая нога)",
        "Тренировка 3:\n1. Скручивания с поднятыми ногами: 3 подхода по 15 повторений\n2. Горизонтальные ножницы: 3 подхода по 20 повторений\n3. Боковая планка: 3 подхода по 20 секунд (каждая сторона)"
    ]
    rand_tr = random.choice(training_list)
    await message.answer(f"Это ваша мини-тренировка на сегодня {rand_tr}")
    tts=gTTS(text=rand_tr,lang='ru')
    tts.save("training.mp3")
    audio=FSInputFile("training.mp3")
    await bot.send_audio(message.chat.id, audio)
    os.remove("training.mp3")

@dp.message(Command('weather'))
async def weater(message: Message):
    await message.answer("Введите название города")

@dp.message()
async def weather_in_city(message: Message):
    if message.text[0:8]!="weather:":
        translator = Translator()
        text_for_translate = message.text
        text_en = translator.translate(text_for_translate, dest='en').text
        await message.answer(text_en)
        await message.answer_voice(text_en)
    else:
        city = message.text[8:]
        weather = get_weather(city)
        if weather.get("cod") != 200:
            await message.answer(f"Не удалось получить погоду для города {city}. Проверьте правильность написания.")
        else:
            str = (
                f"Прогноз погоды в {weather['name']}:\n"
                f"Температура: {weather['main']['temp']}°C\n"
                f"Описание погоды: {weather['weather'][0]['description']}"
            )
            await message.answer(str)


def get_weather(city):
    api_key = '83ae226b645257424cfc78b3aa9e1aed'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    return response.json()



async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

