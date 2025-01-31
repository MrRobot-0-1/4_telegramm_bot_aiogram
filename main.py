import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher


bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Напиши мне название города и я пришлю сводку погоды!")


@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Thunderstorm": "Гроза \U0001F329",
        "Drizzle": "Моросящий дождь \U0001F326",
        "Rain": "Дождь \U0001F327",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B",
        "Smoke": "Дым \U0001F32B",
        "Haze": "Дымка \U0001F32B",
        "Dust sand": "Вихри песка / пыли \U0001F32B",
        "Fog": "Туман \U0001F32B",
        "Sand": "Песок \U0001F32B",
        "Dust": "Пыль \U0001F32B",
        "Ash": "Вулканический пепел \U0001F32B",
        "Squall": "Шквал \U0001F32B",
        "Tornado": "Торнадо \U0001F32B",
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
    }

    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        # pprint(data)

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, не пойму что там за погода!"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        await message.reply(f"### {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ###\n"
              f"# Погода в городе {city} #\n{wd}\nТемпература: {cur_weather}°C\n"
              f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
              f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\n"
              f"Продолжительность дня: {length_of_the_day}\n"
              f"Хорошего дня! \U0001F600"
              )

    except:
        await message.reply("\U0001F928 Проверьте название города \U0001F928")


if __name__ == '__main__':
    executor.start_polling(dp)
